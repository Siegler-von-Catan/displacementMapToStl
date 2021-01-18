#     displacementMapToStl - Transforming a displacement map to a stl model with blender.
#     Copyright (C) 2021
#     Joana Bergsiek, Leonard Geier, Lisa Ihde, Tobias Markus, Dominik Meier, Paul Methfessel
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import bpy
import sys

# command line arguments
# how to use: blender --background empty.blend --python displacementMapToStl.py -- <input_path> <output_path> (both absolute) 
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

input_path = argv[0]
output_path = argv[1]
input_file = input_path.split("\\")[-1]

# add plane to world
bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, -17.85, 0), rotation=(1.5708, 0, 0))

# scale to fit into wax blank model
bpy.ops.transform.resize(value=(7.53201, 7.53201, 7.53201), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)

# create texture with displacement map texture
texture = bpy.data.textures.new("DisplacementMap", "IMAGE")

bpy.ops.image.open(filepath=input_path)

texture.image = bpy.data.images[input_file]

# subdivide for detail in the displacement map
bpy.ops.object.editmode_toggle()

for i in range (0, 9):
    bpy.ops.mesh.subdivide(quadcorner='INNERVERT')

bpy.ops.object.editmode_toggle()

# add displacement modifier
bpy.ops.object.modifier_add(type='DISPLACE')
bpy.context.object.modifiers["Displace"].strength = -0.1875
bpy.context.object.modifiers["Displace"].mid_level = 0.445
bpy.context.object.modifiers["Displace"].texture = texture

# add smoothing
bpy.ops.object.modifier_add(type='CORRECTIVE_SMOOTH')
bpy.context.object.modifiers["CorrectiveSmooth"].factor = 1
bpy.context.object.modifiers["CorrectiveSmooth"].iterations = 15

# finally decrease face countwith decimate modifier
bpy.ops.object.modifier_add(type='DECIMATE')
bpy.context.object.modifiers["Decimate"].ratio = 0.2

# boolean substract on the wax stamp model of 

# import wax stamp model 
# Wax stamp set (http://www.thingiverse.com/thing:3539505) by Cailem042 is licensed under the Creative Commons - Attribution - Share Alike license.
#http://creativecommons.org/licenses/by-sa/3.0/
bpy.ops.import_mesh.stl(filepath="..\\assets\\Wax_Stamp_Blank.stl")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Plane"]
bpy.context.object.modifiers["Boolean"].operation = "DIFFERENCE"
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

# save result
bpy.ops.export_mesh.stl(filepath=output_path, use_selection=True)