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
import os

def determineOutputPath(input_file, output_path):
    output_file = os.path.basename(output_path)
    # just the folder was given
    if not output_file:
        return output_path + input_file.split(".")[0] + ".stl"
    
    # auto complete ".stl"
    file_base_name = output_file.split(".")[0]
    output_path = output_path[:-len(output_file)]
    
    return output_path + file_base_name + ".stl"

def addDisplacementModifier(texture):
    bpy.ops.object.modifier_add(type='DISPLACE')
    bpy.context.object.modifiers["Displace"].strength = -0.14
    bpy.context.object.modifiers["Displace"].texture = texture
    bpy.context.object.modifiers["Displace"].mid_level = 0
    
def addSmoothingModifier():
    bpy.ops.object.modifier_add(type='CORRECTIVE_SMOOTH')
    bpy.context.object.modifiers["CorrectiveSmooth"].factor = 1.0
    bpy.context.object.modifiers["CorrectiveSmooth"].iterations = 25
    bpy.context.object.modifiers["CorrectiveSmooth"].use_pin_boundary = True
    bpy.context.object.modifiers["CorrectiveSmooth"].smooth_type = 'LENGTH_WEIGHTED'


def subdividePlane(runs):
    bpy.ops.object.editmode_toggle()

    for i in range (0, runs):
        bpy.ops.mesh.subdivide(quadcorner='INNERVERT')

    bpy.ops.object.editmode_toggle()
    
def addDecimateFacesModifier(ratio):
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].ratio = ratio
    
def addBooleanSubstractModifier():
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Plane"]
    bpy.context.object.modifiers["Boolean"].operation = "DIFFERENCE"
    bpy.context.object.modifiers["Boolean"].solver = 'FAST'
    
def normalizeZDimension():
     bpy.data.objects["Plane"].dimensions.z = 1.5
    
# command line arguments
# how to use: blender --background empty.blend --python displacementMapToStl.py -- <input_path> <output_path> (both absolute) -lowquality (optional)
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

input_path = argv[0]
input_file = os.path.basename(input_path)
output_path = determineOutputPath(input_file, argv[1])
decimate_factor = 0.069 if len(argv) == 3 else 0.42

# add plane to world
bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, -16.7, 0), rotation=(-1.5708, 3.1416, 0))

# scale to fit into wax blank model
bpy.ops.transform.resize(value=(8, 8, 8), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)

# create texture with displacement map texture
texture = bpy.data.textures.new("DisplacementMap", "IMAGE")

bpy.ops.image.open(filepath=input_path)

texture.image = bpy.data.images[input_file]

subdividePlane(9)

addDisplacementModifier(texture)

addSmoothingModifier()

addDecimateFacesModifier(decimate_factor)

normalizeZDimension()

# import wax stamp model 
# Wax stamp set (http://www.thingiverse.com/thing:3539505) by Cailem042 is licensed under the Creative Commons - Attribution - Share Alike license.
# http://creativecommons.org/licenses/by-sa/3.0/
bpy.ops.import_mesh.stl(filepath=bpy.path.abspath("//../assets/Wax_Stamp_Blank.stl"))

addBooleanSubstractModifier()

# save result
bpy.ops.export_mesh.stl(filepath=output_path, use_selection=True)
