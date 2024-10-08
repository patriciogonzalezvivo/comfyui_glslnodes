"""
@author: Patricio Gonzalez Vivo
@title: GLSL Nodes
@nickname: GLSL Nodes
@description: A set of nodes to work with GLSL shaders
"""

from .glsl_editors import GlslEditor, GlslEditorPro
from .glsl_uniforms import GlslUniforms
from .glsl_viewer import GlslViewer
from .glsl_buffers import GlslBuffers
from .glsl_types import *

from .install import *

NODE_CLASS_MAPPINGS = {
    'int': GlslInt,
    'float': GlslFloat,
    'vec2': GlslVec2,
    'vec3': GlslVec3,
    'vec4': GlslVec4,
    'vec2 (pos)': GlslVec2Pos,
    'vec3 (pos)': GlslVec3Pos,
    'vec4 (color)': GlslVec4Color,
    'glslUniforms': GlslUniforms,
    'glslEditor': GlslEditor,
    'glslEditorPro': GlslEditorPro,
    'glslViewer': GlslViewer,
    'glslBuffers': GlslBuffers,
}

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "WEB_DIRECTORY"]