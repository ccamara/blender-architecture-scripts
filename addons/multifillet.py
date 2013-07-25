# -*- coding: utf-8 -*-

# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

# ------ ------
bl_info = {
    'name': 'fillet_multiple',
    'author': '',
    'version': (0, 0, 1),
    'blender': (2, 5, 8),
    'api': 38887,
    'location': '',
    'description': '',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Mesh' }

# ------ ------
import bpy
from bpy.props import FloatProperty, IntProperty
from mathutils import Vector, Matrix
from math import cos, pi, degrees

# ------ ------
def edit_mode_out():      # edit mode out
    bpy.ops.object.mode_set(mode = 'OBJECT')

def edit_mode_in():      # edit mode in
    bpy.ops.object.mode_set(mode = 'EDIT')

def get_mesh_data_():
    edit_mode_out()
    ob_act = bpy.context.active_object
    me = ob_act.data
    edit_mode_in()
    return me

def list_clear_(l):
    l[:] = []
    return l

# ------ ------ ------ ------
def get_adj_v_(list_):
        tmp = {}
        for i in list_:
                try:             tmp[i[0]].append(i[1])
                except KeyError: tmp[i[0]] = [i[1]]
                try:             tmp[i[1]].append(i[0])
                except KeyError: tmp[i[1]] = [i[0]]
        return tmp

def f_1(frst, list_):      # frst - firts vert in path, list_ - list of edges
    fi = frst
    tmp = [frst]
    while list_ != []:
        for i in list_:
            if i[0] == fi:
                tmp.append(i[1])
                fi = i[1]
                list_.remove(i)
            elif i[1] == fi:
                tmp.append(i[0])
                fi = i[0]
                list_.remove(i)
    return tmp

# ------ ------
class fm_buf():
    list_path = []      # path

# ------ ------ ------ ------
def f_(me, adj, n):

    list_0 = fm_buf.list_path[:]
    #del fm_buf.list_path
    #list_clear_(fm_buf.list_path)

    dict_0 = get_adj_v_(list_0)
    list_fl = [i for i in dict_0 if (len(dict_0[i]) == 1)]      # first and last vertex of path or nothing if loop

    if len(list_fl) == 0:
        loop = True
        path = False
        frst = list_0[0][0]
        list_1 = f_1(frst, list_0)      # list of vertex indices in the same order as they are in the path
        del list_1[-1]      # if loop remove last item from list_1
    else:
        loop = False
        path = True
        frst = list_fl[0]
        list_1 = f_1(frst, list_0)

    v_list = [v.index for v in me.vertices if v.select]
    list_2 = v_list[:]
    list_3 = []
    list_4 = list_1[:]

    dict_2 = {}

    nn = len(list_1)
    for i in list_2:
        if i in list_1:

            j = list_1.index(i)      # index of a item in list_1
            dict_2[list_1[j]] = []
            p = (me.vertices[list_1[j]].co).copy()
            p1 = (me.vertices[list_1[(j - 1) % nn]].co).copy()
            p2 = (me.vertices[list_1[(j + 1) % nn]].co).copy()

            vec1 = p - p1
            vec2 = p - p2

            ang = vec1.angle(vec2, any)

            h = adj * (1 / cos(ang * 0.5))

            p3 = p - (vec1.normalized() * adj)
            p4 = p - (vec2.normalized() * adj)
            rp = p - ((p - ((p3 + p4) * 0.5)).normalized() * h)

            vec3 = rp - p3
            vec4 = rp - p4

            axis = vec1.cross(vec2)

            rot_ang = vec3.angle(vec4)

            for o in range(n + 1):
                new_angle = rot_ang * o / n
                mtrx = Matrix.Rotation(new_angle, 3, axis)
                tmp = p4 - rp
                tmp1 = mtrx*tmp
                tmp2 = tmp1 + rp
                me.vertices.add(1)
                me.vertices[-1].co = tmp2
                me.vertices[-1].select = False
                list_3.append(me.vertices[-1].index)

            k = list_4.index(i)
            list_3.reverse()
            list_4[k:(k + 1)] = list_3
            list_clear_(list_3)

    n1 = len(list_4)
    for t in range(n1):
        a = list_4[t]
        b = list_4[(t + 1) % n1]
        me.edges.add(1)
        me.edges[-1].vertices = [a, b]



# ------ panel 0 ------
class fm_p0(bpy.types.Panel):

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    #bl_idname = 'fm_p0_id'
    bl_label = 'Fillet multiple'
    bl_context = 'mesh_edit'

    def draw(self, context):
        layout = self.layout
        row = layout.split(0.60)
        row.label('Store data :')
        row.operator('fm.op0_id', text = 'Path')
        layout.operator('fm.op1_id', text = 'Fillet multiple')

# ------ operator 0 ------
class fm_op0(bpy.types.Operator):
    bl_idname = 'fm.op0_id'
    bl_label = ''

    def execute(self, context):
        me = get_mesh_data_()
        list_clear_(fm_buf.list_path)
        fm_buf.list_path = [ list(e.key) for e in me.edges if e.select ]
        bpy.ops.mesh.select_all(action = 'DESELECT')
        return {'FINISHED'}

# ------ operator 1 ------
class fm_op1(bpy.types.Operator):

    bl_idname = 'fm.op1_id'
    bl_label = ''
    bl_options = {'REGISTER', 'UNDO'}

    adj = FloatProperty( default = 0.08, min = 0.00001, max = 100.0, step = 1, precision = 3 )
    n = IntProperty( name = '', default = 4, min = 3, max = 100, step = 1 )

    def execute(self, context):

        adj = self.adj
        n = self.n

        edit_mode_out()
        ob_act = context.active_object
        me = ob_act.data
        # -- -- -- --

        f_(me, adj, n)

        # -- -- -- --
        edit_mode_in()
        bpy.ops.mesh.delete(type = 'VERT')
        return {'FINISHED'}

# ------ ------
class_list = [ fm_p0, fm_op0, fm_op1]

# ------ register ------
def register():
    for c in class_list:
        bpy.utils.register_class(c)

# ------ unregister ------
def unregister():
    for c in class_list:
        bpy.utils.unregister_class(c)

# ------ ------
if __name__ == "__main__":
    register()