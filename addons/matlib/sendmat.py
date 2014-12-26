import bpy
with bpy.data.libraries.load("") as (data_from, data_to):
 data_to.materials = ["Test"]
mat = bpy.data.materials["Test"]
mat.use_fake_user=True
bpy.ops.wm.save_mainfile(filepath="D:\\Blender Foundation\\2.62\\scripts\\addons\\matlib\\materials.blend", check_existing=False, compress=True)
