import platform
import moderngl
import numpy as np

from .glsl_texture import ImageTexture, ImageArrayTexture
from .glsl_utils import GL_BACKENDS, GL_PLATFORMS
from .glsl_utils import getDefaultVertexShader, getFragmentShader

class Context:
    def __init__(self):
        self.ctx = None
        self.defines = []
        self.uniforms = {}
        self.textures = []

        backend_os = platform.system()
        if backend_os in GL_BACKENDS:
            self.ctx = moderngl.create_context(
                standalone=True,
                backend=GL_BACKENDS[backend_os],
            )
        else:
            self.ctx = moderngl.create_standalone_context()

        # add first define
        if backend_os in GL_PLATFORMS:
            self.defines.append((GL_PLATFORMS[backend_os], ""))
        

    def setTexture(self, name, image):
        if len(image) is 1:
            tex = ImageTexture(image.numpy()[0], name)
            self.textures.append( tex )
            self.uniforms[f"{name}Resolution"] = (float(tex.width), float(tex.height))
            self.defines.append((f"{name.upper()}_TYPE", "sampler2D"))
        else:
            tex = ImageArrayTexture(image.numpy(), name)
            self.textures.append( tex )
            self.uniforms[f"{name}Resolution"] = (float(tex.width), float(tex.height))
            self.uniforms[f"{name}TotalFrames"] = float(tex.totalFrames)
            self.defines.append((f"{name.upper()}_TOTALFRAMES", float(tex.totalFrames)))
            self.defines.append((f"{name.upper()}_TYPE", "sampler2DArray"))


    def loadTextures(self, images: dict):
        for key, value in images.items():
            if value is not None:
                if len(value) is 1:
                    tex = ImageTexture(value.numpy()[0], key)
                    self.textures.append( tex )
                    self.uniforms[f"{key}Resolution"] = (float(tex.width), float(tex.height))
                    self.defines.append((f"{key.upper()}_TYPE", "sampler2D"))
                else:
                    tex = ImageArrayTexture(value.numpy(), key)
                    self.textures.append( tex )
                    self.uniforms[f"{key}Resolution"] = (float(tex.width), float(tex.height))
                    self.uniforms[f"{key}TotalFrames"] = float(tex.totalFrames)
                    self.defines.append((f"{key.upper()}_TOTALFRAMES", float(tex.totalFrames)))
                    self.defines.append((f"{key.upper()}_TYPE", "sampler2DArray"))
    

    def setUniform(self, name, value):
        if type(value) is int or type(value) is float:
            self.uniforms[name] = value
            self.defines.append((f"{name.upper()}_TYPE", "float"))
        elif type(value) is list or type(value) is tuple:
            self.uniforms[name] = value
            self.defines.append((f"{name.upper()}_TYPE", "vec" + str(len(value))))


    def loadUniforms(self, values):
        for key, value in values.items():
            if value is not None:
                if type(value) is int or type(value) is float:
                    self.uniforms[key] = value
                    self.defines.append((f"{key.upper()}_TYPE", "float"))
                elif type(value) is list or type(value) is tuple:
                    self.uniforms[key] = value
                    self.defines.append((f"{key.upper()}_TYPE", "vec" + str(len(value))))


    def makeProgram(self, fragment_code: str, vertex_code=None, geometry=None):
        if vertex_code is None:
            vertex_code= getDefaultVertexShader(fragment_code["version"])
        
        return self.ctx.program(    vertex_shader=vertex_code,
                                    fragment_shader=getFragmentShader(fragment_code, self.defines) )


    def makeBillboard(self, program):
        vbo = self.ctx.buffer(np.array([
                                            # First triangle
                                            -1.0, -1.0, 
                                            -1.0,  1.0,
                                                1.0,  1.0,
                                            # Second triangle
                                            -1.0, -1.0,
                                                1.0,  1.0,
                                                1.0, -1.0,
                                        ], dtype='f4'))
        return self.ctx.simple_vertex_array(program, vbo, 'a_position')


    def useTextures(self, program):
        for i, texture in enumerate(self.textures):
            texture.use(i, program)


    def useUniforms(self, program):
        for key, value in self.uniforms.items():
            if key in program:
                if value is not None:
                    program[key] = value
