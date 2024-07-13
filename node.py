import moderngl
import requests
import re

import numpy as np
import comfy.utils
from torchvision.transforms import PILToTensor
from PIL import Image
import torch

import comfy.utils

fragment_shader="""#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
varying vec2 v_texcoord;

void main() {
    vec2 pixel = 1.0 / u_resolution;
    vec2 st = gl_FragCoord.xy * pixel;
    vec2 uv = v_texcoord;
    gl_FragColor = vec4(uv, 0.0, 1.0);
}
"""

def resolveLygia(src: str):
    source = ""
    lines = src.split("\n")
    for line in lines:
        # resolve #include dependencies
        match = re.search(r'#include\s*["|<](.*.glsl)["|>]', line, re.IGNORECASE)
        if match:
            url = match.group(1)
            print("Adding dependecy", url)
            if url.startswith("lygia"):
                url = url.replace("lygia", "https://lygia.xyz")

                response = requests.get(url, headers={
                    "Origin": "ComfyUI Server",
                })
                if response.status_code == 200:
                    source += response.text + "\n"
                else:
                    print("Failed to fetch", url)

        else:
            source += line + "\n"

    return source


class ImageTexture:
    def __init__(self, image):
        self.ctx = moderngl.get_context()
        self.texture = self.ctx.texture(image.shape[1::-1], image.shape[2], image)
        self.sampler = self.ctx.sampler(texture=self.texture)
        self.sampler.filter = (self.ctx.NEAREST, self.ctx.NEAREST)

    def use(self, index):
        self.texture.use(index)
        self.sampler.use(index)


class GlslEditor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "glsl_code": ("STRING", {"multiline": True, "default": fragment_shader}),
            },
        }
    CATEGORY = "GLSL"
    FUNCTION = "main"
    RETURN_TYPES = ("GLSL_CODE", )

    def main(self, glsl_code):
        out = resolveLygia(glsl_code)
        return (out,)


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
                "u_tex": ("IMAGE", { "multi": True }),

                # TODO: add support for vertex shader and 3D models
                # "vertex_shader": ("STRING"),
                # "3D_model": ("3D_MODEL", { "default": None }),
            }
        }
    CATEGORY = "GLSL"
    FUNCTION = "main"

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("images", "mask")

    def main(self, fragment_code, width, height, frames, fps, u_tex=None):

        ctx = moderngl.create_context(
            standalone=True,
            backend='egl',
            # # These are OPTIONAL if you want to load a specific version
            # libgl='libGL.so.1',
            # libegl='libEGL.so.1',
        )

        prog = ctx.program(vertex_shader="""
            #version 100
            
            #ifdef GL_ES
            precision mediump float;
            #endif

            attribute vec2 a_position;
            varying vec2 v_texcoord;
                           
            void main() {
                v_texcoord = a_position * 0.5 + 0.5;
                gl_Position = vec4(a_position, 0.0, 1.0);;
            }
            """,
            fragment_shader= "#version 100\n" + fragment_code)

        # Create a simple billboard quad, where the first 4 floats is the postion followed by the texture coordinates
        vertices = np.array([
            # First triangle
            -1.0, -1.0, 
            -1.0,  1.0,
             1.0,  1.0,
            # Second triangle
            -1.0, -1.0,
             1.0,  1.0,
             1.0, -1.0,
        ], dtype='f4')

        vbo = ctx.buffer(vertices)
        vao = ctx.simple_vertex_array(prog, vbo, 'a_position')

        fboaa = ctx.simple_framebuffer((width, height), components=4, samples=8)
        fboaa.use()
        
        # fbo = ctx.framebuffer(color_attachments=[ctx.texture((width, height), 4)])
        fbo = ctx.simple_framebuffer((width, height), components=4)
        # fbo.use()

        # ctx.clear()

        if 'u_resolution' in vao.program:
            vao.program['u_resolution'] = (float(width), float(height))
        
        if 'u_fps' in vao.program:
            vao.program['u_fps'] = fps

        if u_tex is not None:
            for i, image in enumerate(u_tex):
                name = f"u_tex{i}"
                if name in vao.program:
                    # convert image from torch tensor to numpy array
                    image = image.numpy()
                    image = np.flip(image, 0)
                    image = (image * 255).astype(np.uint8)
                    texture = ImageTexture(image)
                    texture.use(i)
                    vao.program[name] = i

        images_out = []
        masks_out = []
        ptt = PILToTensor()
        pbar = comfy.utils.ProgressBar(frames)
        for i in range(frames):
            if comfy.utils.PROGRESS_BAR_ENABLED:
                pbar.update_absolute(i + 1, frames)

            if 'u_frame' in vao.program:
                vao.program['u_frame'] = i

            if 'u_time' in vao.program:
                vao.program['u_time'] = i / fps

            ctx.clear(0.0, 0.0, 0.0, 0.0)
            vao.render(mode=moderngl.TRIANGLES)

            ctx.copy_framebuffer(dst=fbo, src=fboaa)
            data = fbo.read(components=4)

            image = Image.frombytes("RGBA", fbo.size, data)
            image = ptt(image)

            image = image.permute(1, 2, 0).float().mul(1.0 / 255.0)
            image = image.flip(0)

            images_out.append(image[:, :, :3].unsqueeze(0))
            masks_out.append(image[:, :, 3].squeeze().unsqueeze(0))

        return (torch.cat(images_out, dim=0), torch.stack(masks_out, dim=0))
    
    def IS_CHANGED(self, **kwargs):
        return float("nan")