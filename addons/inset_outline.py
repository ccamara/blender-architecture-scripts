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
    'name': 'inset_edge_chain_loop',
    'author': '',
    'version': (0, 0, 6),
    'blender': (2, 6, 1),
    'api': 43085,
    'location': 'View3D > Tool Shelf',
    'description': '',
    'warning': 'Beta',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Mesh' }

# ------ ------
import bpy
from bpy.props import FloatProperty, BoolProperty
from mathutils.geometry import normal
from mathutils import Vector, Matrix
from math import tan, pi, degrees

# ------ ------
def edit_mode_out():
    bpy.ops.object.mode_set(mode = 'OBJECT')

def edit_mode_in():
    bpy.ops.object.mode_set(mode = 'EDIT')

def get_adj_v_(list_):
        tmp = {}
        for i in list_:
                try:             tmp[i[0]].append(i[1])
                except KeyError: tmp[i[0]] = [i[1]]
                try:             tmp[i[1]].append(i[0])
                except KeyError: tmp[i[1]] = [i[0]]
        return tmp

def f_1(frst, list_, last):      # edge chain
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
        if tmp[-1] == last:
            break
    return tmp

def f_2(frst, list_):      # edge loop
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
        if tmp[-1] == frst:
            break
    return tmp

# ------ ------ ------ ------
def f_(me, list_0, dict_0, opp, list_fl, in_):

    if len(list_fl) == 0:      # loop
        loop = True
        path = False
        frst = list_0[0][0]
        list_1 = f_2(frst, list_0)
        del list_1[-1]

    else:      # path
        loop = False
        path = True
        frst = list_fl[0]
        last = list_fl[1]
        list_1 = f_1(frst, list_0, last)

    n = len(list_1)
    for ii in range(n):
        p_ = (me.vertices[list_1[ii]].co).copy()
        p1_ = (me.vertices[list_1[(ii - 1) % n]].co).copy()
        p2_ = (me.vertices[list_1[(ii + 1) % n]].co).copy()
        vec1_ = p_ - p1_
        vec2_ = p_ - p2_
        ang = vec1_.angle(vec2_, any)
        an = round(degrees(ang))

        if ang == 0 or ang == 180:
            continue
        elif ang != 0 or ang != 180:
            vec_no = normal(p_, p1_, p2_)
            break
        
    list_2 = []
    list_3 = []

    for i in range(n):
        p = (me.vertices[list_1[i]].co).copy()
        p1 = (me.vertices[list_1[(i - 1) % n]].co).copy()
        p2 = (me.vertices[list_1[(i + 1) % n]].co).copy()

        me.vertices[list_1[i]].select = False

        if in_ == True:
            p3 = p - (vec_no * opp)
        else:
            p3 = p + (vec_no * opp)

        me.vertices.add(1)
        me.vertices[-1].co = p3

        list_2.append(list_1[i])
        list_3.append(me.vertices[-1].index)

    n1 = len(list_2)
    if path == True:
        for j in range(n1 - 1):
            me.faces.add(1)
            me.faces[-1].vertices_raw = [ list_2[j], list_2[(j + 1) % n1], list_3[(j + 1) % n1], list_3[j] ]
    elif loop == True:
        for j in range(n1):
            me.faces.add(1)
            me.faces[-1].vertices_raw = [ list_2[j], list_2[(j + 1) % n1], list_3[(j + 1) % n1], list_3[j] ]

    # -- -- -- --
    list_4 = []
    n2 = len(list_2)
    for k in range(n2):

        q = (me.vertices[list_2[k]].co).copy()
        q1 = (me.vertices[list_2[(k - 1) % n2]].co).copy()
        q2 = (me.vertices[list_2[(k + 1) % n2]].co).copy()

        vec1 = q - q1
        vec2 = q - q2

        q3 = q - (vec1.normalized() * 0.1)
        q4 = q - (vec2.normalized() * 0.1)

        ang = vec1.angle(vec2, any)
        
        if path:
            if k == 0:
                axis = vec2
            elif k == n2 - 1:
                axis = -vec1
            else:
                axis = q3 - q4
            
            mtrx = Matrix.Rotation((pi * 0.5), 3, axis)
            q5 = (me.vertices[list_3[k]].co).copy()
            tmp = q5 - q
            tmp1 = mtrx * tmp
            tmp2 = tmp1 + q

            if k == 0:
                list_4.append(tmp2)
            elif k == n2 - 1:
                list_4.append(tmp2)
            else:
                vec3 = tmp2 - q
                adj = opp / tan(ang / 2)
                h = (adj ** 2 + opp ** 2) ** 0.5
                q6 = q + (vec3.normalized() * h)
                list_4.append(q6)

        elif loop:

            axis = q3 - q4
            ang = vec1.angle(vec2, any)

            mtrx = Matrix.Rotation((pi * 0.5), 3, axis)
            q5 = (me.vertices[list_3[k]].co).copy()
            tmp = q5 - q
            tmp1 = mtrx * tmp
            tmp2 = tmp1 + q

            vec3 = tmp2 - q
        
            # -- -- -- --
            d_ = tan(ang / 2)
            if d_ == 0:
                pass
            elif d_ != 0:
                adj = opp / tan(ang / 2)
                h = (adj ** 2 + opp ** 2) ** 0.5
                q6 = q + (vec3.normalized() * h)
                me.vertices[list_3[k]].co = q6
            # -- -- -- --

    if len(list_4) == 0:
        pass
    else:
        for kk in range(n2):
            me.vertices[list_3[kk]].co = list_4[kk]

    me.update(calc_edges = True)

# ------ panel 0 ------
class io_p0(bpy.types.Panel):

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    #bl_idname = 'io_p0_id'
    bl_label = 'Inset outline'
    bl_context = 'mesh_edit'

    def draw(self, context):
        layout = self.layout
        layout.operator('io.op0_id', text = 'Inset outline')

# ------ operator 0 ------
class io_op0(bpy.types.Operator):

    bl_idname = 'io.op0_id'
    bl_label = 'Inset outline'
    bl_options = {'REGISTER', 'UNDO'}

    opp = FloatProperty( name = '', default = 0.06, min = -100.0, max = 100.0, step = 1, precision = 3 )
    in_ = BoolProperty( name = 'in / out', default = False )

    def draw(self, context):
        layout = self.layout
        layout.label('Inset amount:')
        layout.prop(self, 'opp')
        #layout.prop(self, 'in_')
    
    def execute(self, context):
        opp = self.opp
        in_ = self.in_

        edit_mode_out()
        ob_act = context.active_object
        me = ob_act.data
        # -- -- -- --
        
        list_0 = [list(e.key) for e in me.edges if e.select]
        dict_0 = get_adj_v_(list_0)
        
        list_tmp = [i for i in dict_0 if (len(dict_0[i]) > 2)]
        
        list_fl = [i for i in dict_0 if (len(dict_0[i]) == 1)]
        
        if len(list_0) == 0:      # check for empty list
            self.report({'INFO'}, 'No outline selected')
            edit_mode_in()
            return 'CANCELLED'
        elif len(list_0) != 0:
            if len(list_tmp) != 0:      # check if any of the vertices has more than two neighbors
                self.report({'INFO'}, 'Multiple edge chains not supported')
                edit_mode_in()
                return 'CANCELLED'
            elif len(list_tmp) == 0:
                if len(list_fl) > 2:
                    self.report({'INFO'}, 'Select only one edge chain or edge loop')
                elif len(list_fl) <= 2:
                    f_(me, list_0, dict_0, opp, list_fl, in_)
        # -- -- -- --
        edit_mode_in()
        return {'FINISHED'}

# ------ ------
class_list = [ io_op0,io_p0 ]

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