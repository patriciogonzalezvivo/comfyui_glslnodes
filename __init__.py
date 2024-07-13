from .node import *
from .install import *

NODE_CLASS_MAPPINGS = {
    'glslViewer': GlslViewer,
    'glslEditor': GlslEditor,
}

__all__ = ['NODE_CLASS_MAPPINGS']