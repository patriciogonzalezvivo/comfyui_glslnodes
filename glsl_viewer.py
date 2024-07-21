
import platform
from datetime import date

from PIL import Image

import moderngl

from torchvision.transforms import PILToTensor
import torch
import comfy.utils

from .glsl_context import Context

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
                # "vertex_shader": ("STRING"),
                # "3D_model": ("3D_MODEL", { "default": None }),

                "u_tex0": ("IMAGE", { "multi": True }),
                "u_tex1": ("IMAGE", { "multi": True }),
                "u_tex2": ("IMAGE", { "multi": True }),
                "u_tex3": ("IMAGE", { "multi": True }),

                "u_val0": ("*", { "multi": True }),
                "u_val1": ("*", { "multi": True }),
                "u_val2": ("*", { "multi": True }),
                "u_val3": ("*", { "multi": True }),
            }
        }
    
    CATEGORY = "GLSL"
    FUNCTION = "main"

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("images", "mask")

    def main(self, fragment_code, width, height, frames, fps, **kwargs):
        print("Optional Inputs", kwargs.keys())

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
        
        # Create Shader Program
        prog = context.makeProgram(fragment_code, vertex_code=vertex_code, geometry=geometry)

        # Create a simple billboard 
        vao = context.makeBillboard(prog)

        # TODO: make sure this is the best way to get aMSA buffer
        fboaa = context.ctx.simple_framebuffer((width, height), components=4, samples=8)
        fboaa.use()
        # fbo = ctx.framebuffer(color_attachments=[ctx.texture((width, height), 4)])
        fbo = context.ctx.simple_framebuffer((width, height), components=4)

        # Render Loop
        masks_out = []
        images_out = []
        ptt = PILToTensor()
        pbar = comfy.utils.ProgressBar(frames)

        # Bind Textures
        context.useTextures(vao.program)
        
        for i in range(frames):

            # Update Progress Bar
            if comfy.utils.PROGRESS_BAR_ENABLED:
                pbar.update_absolute(i + 1, frames)

            # Update dynamic uniforms
            context.uniforms['u_frame'] = int(i)
            context.uniforms['u_time'] = float(i / fps)

            # Set Uniforms
            context.useUniforms(vao.program)

            # Render Call
            context.ctx.clear(0.0, 0.0, 0.0, 0.0)
            vao.render(mode=moderngl.TRIANGLES)

            # Copy Framebuffer to MSA
            context.ctx.copy_framebuffer(dst=fbo, src=fboaa)
            data = fbo.read(components=4)

            # Extract Image
            image = Image.frombytes("RGBA", fbo.size, data)
            image = ptt(image)

            image = image.permute(1, 2, 0).float().mul(1.0 / 255.0)
            image = image.flip(0)

            # Append to outputs
            images_out.append(image[:, :, :3].unsqueeze(0))
            masks_out.append(image[:, :, 3].squeeze().unsqueeze(0))

        # Close Context
        return (torch.cat(images_out, dim=0), torch.stack(masks_out, dim=0))
    
    # def IS_CHANGED(self, **kwargs):
    #     return float("nan")