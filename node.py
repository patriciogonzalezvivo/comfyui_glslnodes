import moderngl
import requests
import re

import numpy as np
import torch

fragment_shader="""
#ifdef GL_ES
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
                
                response = requests.get(url)
                if response.status_code == 200:
                    source += response.text + "\n"
                else:
                    print("Failed to fetch", url)

        else:
            source += line + "\n"

    return source


class GlslNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", { "default": 512 }),
                "height": ("INT", { "default": 512 }),
                "fragment_shader": ("STRING", {"multiline": True, "default": fragment_shader}),
            }
        }
    CATEGORY = "GlslNode"
    FUNCTION = "main"
    RETURN_TYPES = ("IMAGE", )

    def main(self, width, height, fragment_shader):
        fragment_shader = resolveLygia(fragment_shader)

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
            fragment_shader= "#version 100\n" + fragment_shader)

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
        fbo = ctx.framebuffer(
            color_attachments=[ctx.texture((width, height), 4)]
        )

        fbo.use()
        ctx.clear()

        if 'u_resolution' in vao.program:
            vao.program['u_resolution'] = (float(width), float(height))

        vao.render()

        data = fbo.read(components=4)

        np_image = np.frombuffer(data, dtype=np.uint8).reshape((*fbo.size[1::-1], 4))
        
        # flip image in Y the X axis
        np_image = np.flip(np_image, 0)

        image = np.array(np_image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        
        return (image, )