import bpy
import sys

# command line arguments
# how to use: blender --background empty.blend --python displacementMapToStl.py -- <input_path> <output_path> (both relative)
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

input_path = argv[0]
output_path = argv[1]
input_file = input_path.split("\\")[-1]

# add plane to world
bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, -19, 0), rotation=(1.5708, 0, 0))

# scale to fit into wax blank model
bpy.ops.transform.resize(value=(9, 9, 9), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)

# create texture with displacement map texture
texture = bpy.data.textures.new("DisplacementMap", "IMAGE")
bpy.ops.image.open(filepath=input_path, relative_path=True)

texture.image = bpy.data.images[input_file]

# subdivide for detail in the displacement map
bpy.ops.object.editmode_toggle()

for i in range (0, 8):
    bpy.ops.mesh.subdivide(quadcorner='INNERVERT')

bpy.ops.object.editmode_toggle()

# add & apply displacement modifier
bpy.ops.object.modifier_add(type='DISPLACE')
bpy.context.object.modifiers["Displace"].strength = -1
bpy.context.object.modifiers["Displace"].mid_level = 0.3
bpy.context.object.modifiers["Displace"].texture = texture
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Displace")

# add & apply smooth laplacian modifier
bpy.ops.object.modifier_add(type='LAPLACIANSMOOTH')
bpy.context.object.modifiers["Laplacian Smooth"].lambda_factor = 8
bpy.context.object.modifiers["Laplacian Smooth"].lambda_border = 8
bpy.context.object.modifiers["Laplacian Smooth"].iterations = 20
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Laplacian Smooth")

# add & apply smooth moidifier
bpy.ops.object.modifier_add(type='SMOOTH')
bpy.context.object.modifiers["Smooth"].factor = 1.3
bpy.context.object.modifiers["Smooth"].iterations = 15
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Smooth")

# finally decrease face countwith decimate modifier
bpy.ops.object.modifier_add(type='DECIMATE')
bpy.context.object.modifiers["Decimate"].ratio = 0.3
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

# boolean substract on the wax stamp model of 

# import wax stamp model 
# Wax stamp set (http://www.thingiverse.com/thing:3539505) by Cailem042 is licensed under the Creative Commons - Attribution - Share Alike license.
http://creativecommons.org/licenses/by-sa/3.0/
bpy.ops.import_mesh.stl(filepath="..\\assets\\Wax_Stamp_Blank.stl")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Plane"]
bpy.context.object.modifiers["Boolean"].operation = "DIFFERENCE"
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

# save result
bpy.ops.export_mesh.stl(filepath=output_path, use_selection=True)