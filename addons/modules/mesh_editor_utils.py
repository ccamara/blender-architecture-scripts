# -*- coding: utf-8 -*-
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

'''
    mesh_editor_utils.py
    
    Helper methods for modifying meshes...



'''


import bpy



# Modify mesh data
class MeshEditor:

    @classmethod
    def addVertex(cls, v):
        toggle = False
        if bpy.context.mode == 'EDIT_MESH':
            toggle = True
        if toggle:
            bpy.ops.object.editmode_toggle()
        mesh = bpy.context.active_object.data
        mesh.add_geometry (1, 0, 0)
        vi = len (mesh.vertices) - 1
        mesh.vertices[vi].co = v
        mesh.update()
        if toggle:
            bpy.ops.object.editmode_toggle()
        return vi
        
    @classmethod
    def addEdge(cls, vi1, vi2):
        toggle = False
        if bpy.context.mode == 'EDIT_MESH':
            toggle = True
        if toggle:
            bpy.ops.object.editmode_toggle()
        mesh = bpy.context.active_object.data
        mesh.add_geometry (0, 1, 0)
        ei = len (mesh.edges) - 1
        e = mesh.edges[ei]
        e.vertices[0] = vi1;
        e.vertices[1] = vi2;
        mesh.update()
        if toggle:
            bpy.ops.object.editmode_toggle()
        return ei
