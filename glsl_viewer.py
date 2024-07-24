from datetime import date
import re

import moderngl

from torchvision.transforms import PILToTensor
import torch
import comfy.utils

from .glsl_context import Context
from .glsl_buffers import Buffer, DoubleBuffer
from .glsl_utils import getSizeFromCode

class GlslViewer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "fragment_code": ("GLSL_CODE", { "dynamicPrompts": False }),
                "width": ("INT", { "default": 512 }),
                "height": ("INT", { "default": 512 }),
                "frames": ("INT", { "default": 1 }),
                "fps": ("INT", { "default": 30 }),
            },
            "optional": {
                # TODO: add support for vertex shader and 3D models
                # "vertex_code": ("GLSL_CODE", { "dynamicPrompts": False }),
                # "3D_model": ("3D_MODEL", { "default": None }),
                "uniforms": ("GLSL_CONTEXT",),
            }
        }
    
    CATEGORY = "GLSL"
    FUNCTION = "main"

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("images", "mask")

    def main(self, fragment_code, width, height, frames, fps, **kwargs):
        # print("Optional Inputs", kwargs.keys())

        context = None
        geometry = None
        vertex_code = None
        images_in = {}
        values_in = {}

        for key, value in kwargs.items():
            if key.startswith("uniforms"):
                context = value
            elif key.startswith("u_tex"):
                images_in[key] = value
            elif key.startswith("u_val"):
                values_in[key] = value

        if context is None:
            context = Context()

        context.loadTextures(images_in)
        context.loadUniforms(values_in)

        context.setUniform("u_date", (float(date.today().year), float(date.today().month), float(date.today().day), (date.today() - date.today()).total_seconds()))
        context.setUniform("u_resolution", (float(width), float(height)) )
        context.setUniform("u_time", 0.0)
        context.setUniform("u_delta", 1.0 / fps)
        context.setUniform("u_fps", fps)
        context.setUniform("u_frame", 0)
        
        # Create a Scene Buffer
        sceneBuffer = DoubleBuffer(width, height, "u_scene", ctx=context.ctx)

        buffers = []
        DoubleBuffers = []

        # Create buffers and VAOs for each appearence of #ifdef BUFFER_<X>
        found_buffers = re.findall(r'(?:^\s*)((?:#if|#elif)(?:\s*)(defined\s*\(\s*BUFFER_)(\d+)(?:\s*\))|(?:#ifdef)(?:\s*BUFFER_)(\d+)(?:\s*))', fragment_code["src"], re.MULTILINE)
        if found_buffers:
            for match in found_buffers:
                print( match)
                buffer_index = match[2] if match[2] is not '' else match[3]
                buffer_name = f"u_buffer{buffer_index}"
                buffer_size = getSizeFromCode(width, height, fragment_code["src"], buffer_name)
                buffer_code = fragment_code.copy()
                buffer_code["src"] = f"#define BUFFER_{buffer_index}\n" + buffer_code["src"]
                print("Creating Buffer", buffer_name, buffer_size)
                buffers.append( (Buffer(buffer_size[0], buffer_size[1], buffer_name, ctx=context.ctx), 
                                 context.makeCanvasShader(buffer_code) ) )

        found_double_buffers = re.findall(r'(?:^\s*)((?:#if|#elif)(?:\s*)(defined\s*\(\s*DOUBLE_BUFFER_)(\d+)(?:\s*\))|(?:#ifdef)(?:\s*DOUBLE_BUFFER_)(\d+)(?:\s*))', fragment_code["src"], re.MULTILINE)
        if found_double_buffers:
            for match in found_double_buffers:
                buffer_index = match[2] if match[2] is not '' else match[3]
                buffer_name = f"u_doubleBuffer{buffer_index}"
                buffer_size = getSizeFromCode(width, height, fragment_code["src"], buffer_name)
                buffer_code = fragment_code.copy()
                buffer_code["src"] = f"#define DOUBLE_BUFFER_{buffer_index}\n" + buffer_code["src"]
                print("Creating Double Buffer", buffer_name, buffer_size)
                DoubleBuffers.append( (DoubleBuffer(buffer_size[0], buffer_size[1], buffer_name, ctx=context.ctx), 
                                       context.makeCanvasShader(buffer_code) ) )
            
        # Create Shader Program
        vao = context.makeCanvasShader(fragment_code)

        # Render Loop
        masks_out = []
        images_out = []
        ptt = PILToTensor()
        pbar = comfy.utils.ProgressBar(frames)

        # Execute Render Loop for each frame
        for i in range(frames):

            # Update Progress Bar
            if comfy.utils.PROGRESS_BAR_ENABLED:
                pbar.update_absolute(i + 1, frames)

            # Update dynamic uniforms
            context.uniforms['u_frame'] = int(i)
            context.uniforms['u_time'] = float(i / fps)

            #### BUFFER RENDER PASSES ####
            for buffer, buffer_vao in buffers:
                buffer.bind()

                # Set Uniforms
                context.useUniforms(vao.program)

                # Bind Textures
                textureIndex = context.useTextures(vao.program)

                # bind buffer textures (skip current buffer)
                for buffer2, buffer_vao2 in buffers:
                    if buffer2.name != buffer.name:
                        buffer2.use(textureIndex, buffer_vao2.program)
                        textureIndex += 1

                for buffer2, buffer_vao2 in DoubleBuffers:
                    buffer2.use(textureIndex, buffer_vao2.program)
                    textureIndex += 1

                context.ctx.clear(0.0, 0.0, 0.0, 0.0)
                buffer_vao.render(mode=moderngl.TRIANGLES)

            for buffer, buffer_vao in DoubleBuffers:
                buffer.bind()

                # Set Uniforms
                context.useUniforms(vao.program)

                # Bind Textures
                textureIndex = context.useTextures(vao.program)

                # bind buffer textures (skip current buffer)
                for buffer2, buffer_vao2 in buffers:
                    buffer2.use(textureIndex, buffer_vao2.program)
                    textureIndex += 1
                
                for buffer2, buffer_vao2 in DoubleBuffers:
                    buffer2.use(textureIndex, buffer_vao2.program, prev=True)
                    textureIndex += 1

                context.ctx.clear(0.0, 0.0, 0.0, 0.0)
                buffer_vao.render(mode=moderngl.TRIANGLES)


            #### MAIN RENDER PASS ####

            # Bind Buffer
            sceneBuffer.bind()

            # Set Uniforms
            context.useUniforms(vao.program)

            # Bind Textures
            textureIndex = context.useTextures(vao.program)

            # bind buffer textures
            for buffer, buffer_vao in buffers:
                buffer.use(textureIndex, vao.program)
                textureIndex += 1
            
            for buffer, buffer_vao in DoubleBuffers:
                buffer.use(textureIndex, vao.program)
                textureIndex += 1

            # Render Call
            context.ctx.clear(0.0, 0.0, 0.0, 0.0)
            vao.render(mode=moderngl.TRIANGLES)


            #### OUTPUT PASS ####

            # get Image in to torch tensor
            image = sceneBuffer.getImage()
            image = ptt(image)

            image = image.permute(1, 2, 0).float().mul(1.0 / 255.0)
            image = image.flip(0)

            # Append to outputs
            images_out.append(image[:, :, :3].unsqueeze(0))
            masks_out.append(image[:, :, 3].squeeze().unsqueeze(0))

        # Close Context
        return (torch.cat(images_out, dim=0), torch.stack(masks_out, dim=0))