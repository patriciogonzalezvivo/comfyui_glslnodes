
import platform

import numpy as np
from PIL import Image

import moderngl

from torchvision.transforms import PILToTensor
import torch
import comfy.utils

from .texture import ImageTexture, ImageArrayTexture
from .utils import resolveLygia, stackDefines

backends = {
    "Linux": "egl",
    "Windows": "wgl",
    "Darwin": "cgl",
}

VERSION = "#version 120\n"
PRECISION = """#ifdef GL_ES
precision mediump float;
#endif\n"""

fragment_shader= PRECISION + """ 
uniform vec2 u_resolution;
varying vec2 v_texcoord;

void main() {
    vec2 pixel = 1.0 / u_resolution;
    vec2 st = gl_FragCoord.xy * pixel;
    vec2 uv = v_texcoord;
    gl_FragColor = vec4(uv, 0.0, 1.0);
}
"""

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
                # TODO make this dynamic
                "u_tex0": ("IMAGE", { "multi": True }),
                "u_tex1": ("IMAGE", { "multi": True }),
                "u_tex2": ("IMAGE", { "multi": True }),
                "u_tex3": ("IMAGE", { "multi": True }),

                # TODO make this dynamic
                "u_val0": ("*", { "multi": True, "default": None }),
                "u_val1": ("*", { "multi": True, "default": None }),
                "u_val2": ("*", { "multi": True, "default": None }),
                "u_val3": ("*", { "multi": True, "default": None }),

                # TODO: add support for vertex shader and 3D models
                # "vertex_shader": ("STRING"),
                # "3D_model": ("3D_MODEL", { "default": None }),
            }
        }
    CATEGORY = "GLSL"
    FUNCTION = "main"

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("images", "mask")

    def main(self, fragment_code, width, height, frames, fps, 
             # TODO make this dynamic
             u_tex0=None, u_tex1=None, u_tex2=None, u_tex3=None,
             # TODO make this dynamic
             u_val0=None, u_val1=None, u_val2=None, u_val3=None):

        ctx = None
        backend_os = platform.system()
        if backend_os in backends:
            ctx = moderngl.create_context(
                standalone=True,
                backend=backends[backend_os],
            )
        else:
            ctx = moderngl.create_standalone_context()

        defines = []
        textures = []

        # TODO make this dynamic
        if u_tex0 is not None:
            if len(u_tex0) is 1:
                # convert image from torch tensor to numpy array and then to a Texture
                textures.append( ImageTexture(u_tex0.numpy()[0], "u_tex0") )
            else:
                textures.append( ImageArrayTexture(u_tex0.numpy(), "u_tex0", defines) )

        if u_tex1 is not None:
            if len(u_tex1) is 1:
                # convert image from torch tensor to numpy array and then to a Texture
                textures.append( ImageTexture(u_tex1.numpy()[0], "u_tex1") )
            else:
                textures.append( ImageArrayTexture(u_tex1.numpy(), "u_tex1", defines) )

        if u_tex2 is not None:
            if len(u_tex2) is 1:
                # convert image from torch tensor to numpy array and then to a Texture
                textures.append( ImageTexture(u_tex2.numpy()[0], "u_tex2") )
            else:
                textures.append( ImageArrayTexture(u_tex2.numpy(), "u_tex2", defines) )

        if u_tex3 is not None:
            if len(u_tex3) is 1:
                # convert image from torch tensor to numpy array and then to a Texture
                textures.append( ImageTexture(u_tex3.numpy()[0], "u_tex3") )
            else:
                textures.append( ImageArrayTexture(u_tex3.numpy(), "u_tex3", defines) )

        prog = ctx.program(vertex_shader=VERSION + PRECISION + """
            attribute vec2 a_position;
            varying vec2 v_texcoord;
                           
            void main() {
                v_texcoord = a_position * 0.5 + 0.5;
                gl_Position = vec4(a_position, 0.0, 1.0);;
            }
            """,
            fragment_shader= VERSION + 
                             stackDefines(defines) + 
                             "\n#line 1\n" +
                             fragment_code)

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

        
        # TODO make this dynamic
        if u_val0 is not None and 'u_val0' in vao.program:
            if type(u_val0) is int or type(u_val0) is float:
                vao.program['u_val0'] = u_val0
            elif type(u_val0) is list or type(u_val0) is tuple:
                vao.program['u_val0'] = u_val0

        if u_val1 is not None and 'u_val1' in vao.program:
            if type(u_val1) is int or type(u_val1) is float:
                vao.program['u_val1'] = u_val1
            elif type(u_val1) is list or type(u_val1) is tuple:
                vao.program['u_val1'] = u_val1

        if u_val2 is not None and 'u_val2' in vao.program:
            if type(u_val2) is int or type(u_val2) is float:
                vao.program['u_val2'] = u_val2
            elif type(u_val2) is list or type(u_val2) is tuple:
                vao.program['u_val2'] = u_val2

        if u_val3 is not None and 'u_val3' in vao.program:
            if type(u_val3) is int or type(u_val3) is float:
                vao.program['u_val3'] = u_val3
            elif type(u_val3) is list or type(u_val3) is tuple:
                vao.program['u_val3'] = u_val3

        images_out = []
        masks_out = []
        ptt = PILToTensor()
        pbar = comfy.utils.ProgressBar(frames)
        for i in range(frames):
            if comfy.utils.PROGRESS_BAR_ENABLED:
                pbar.update_absolute(i + 1, frames)

            if 'u_frame' in vao.program:
                vao.program['u_frame'] = int(i)

            if 'u_time' in vao.program:
                vao.program['u_time'] = float(i / fps)

            # Bind Textures
            texture_index = 0
            for i, texture in enumerate(textures):
                texture.use(texture_index, vao.program)


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
    
    # def IS_CHANGED(self, **kwargs):
    #     return float("nan")