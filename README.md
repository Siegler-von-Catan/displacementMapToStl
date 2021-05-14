# displacementMapToStl
Transforms a displacement map / height map to a 3D model and applies it on a 3D stamp mocel provided as CC BY SA by Cailem042.

## Instruction
You need blender version >= 2.91 

## Usage
Go to the directory "src" which contains the script and execute:

`blender --background empty.blend --python displacementMapToStl.py -- <input_path> <output_path> (both absolute) -lowquality (optional)`

Make sure blender is part of your system environment variables.

## Supported Input
The program accepts any image format that blender can turn into a texture (see https://docs.blender.org/manual/en/2.91/files/media/image_formats.html). 

Your image should have a white border (white == highest point in heightmap) as you might get an empty stamp otherwise. Since most of our data is cropped as circles, we scale the image slightly larger than the stamp's available space. This results in squared images leaving edges beyond the stamp's lowering. The attached image below displays that optimal usage is achieved by circle-corpping your image.

![alt text](https://github.com/Siegler-von-Catan/displacementMapToStl/blob/master/comparingInputs.png)