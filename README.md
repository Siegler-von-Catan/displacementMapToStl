# Displacement Map (Height Map) To Stl
Applies a displacement map / height map to a 3D stamp model provided as CC BY SA by Cailem042, resulting in the height map being the motive of the stamp.

## Instruction
You need blender version >= 2.91 

## Usage
Go to the directory "src" which contains the script and execute:

`blender --background empty.blend --python displacementMapToStl.py -- <input_path> <output_path> (both absolute) -lowquality (optional)`

Make sure blender is part of your system environment variables.

## Supported Input
The program accepts any image format that blender can turn into a texture (see https://docs.blender.org/manual/en/2.91/files/media/image_formats.html). 

Your greyscale image should have a white border (white == highest point in heightmap) as you might get an empty stamp otherwise. Since most of our data is cropped in circles, we scale the image slightly larger than the stamp's available space. This results in squared images leaving edges beyond the stamp's lowering. The attached image below displays that optimal usage is achieved by circle-cropping your image.

![alt text](https://github.com/Siegler-von-Catan/displacementMapToStl/blob/master/comparingInputs.png)
