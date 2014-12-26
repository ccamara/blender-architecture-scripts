import bpy
mat = bpy.data.materials["Material"]
mat.name = "tmp"
mat.user_clear()
with bpy.data.libraries.load("untitled.blend") as (data_from, data_to):
 data_to.materials = ["Material"]
mat = bpy.data.materials["Material"]
mat.use_fake_user=True
bpy.ops.wm.save_mainfile(filepath="/home/carlinux/.config/blender/2.71/scripts/addons/matlib/materials.blend", check_existing=False, compress=True)
