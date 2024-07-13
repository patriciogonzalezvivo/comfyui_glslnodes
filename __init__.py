"""
@author: Patricio Gonzalez Vivo
@title: GLSL Nodes
@nickname: GLSL Nodes
@description: A set of nodes to work with GLSL shaders
"""

from .node import *
from .install import *

NODE_CLASS_MAPPINGS = {
    'glslViewer': GlslViewer,
    'glslEditor': GlslEditor,
}

__all__ = ['NODE_CLASS_MAPPINGS']