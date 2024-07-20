"""
@author: Patricio Gonzalez Vivo
@title: GLSL Nodes
@nickname: GLSL Nodes
@description: A set of nodes to work with GLSL shaders
"""

from .editors import GlslEditor, GlslShaderToy
from .viewer import GlslViewer
from .types import *

from .install import *

NODE_CLASS_MAPPINGS = {
    'int': GlslInt,
    'float': GlslFloat,
    'vec2': GlslVec2,
    'vec3': GlslVec3,
    'vec4': GlslVec4,
    'glslViewer': GlslViewer,
    'glslEditor': GlslEditor,
    'glslEditor (ShaderToy)': GlslShaderToy,
}

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "WEB_DIRECTORY"]