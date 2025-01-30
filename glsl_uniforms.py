from .glsl_context import Context
import comfy.utils

class GlslUniforms:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                # TODO: add support for vertex shader and 3D models
                # "vertex_shader": ("STRING"),
                # "3D_model": ("3D_MODEL", { "default": None }),
            }
        }
    
    CATEGORY = "GLSL"
    FUNCTION = "main"
    
    RETURN_TYPES = ("GLSL_CONTEXT",)
    RETURN_NAMES = ("uniforms",)
    # DESCRIPTION = """
    # This node caches and optimizes inputs for GlslViewer.
    # And you can connect different inputs like Images (Textures), Videos(Texture Arrays), or individual values (int, float, vec2, vec3, vec4).
    # If you are working with videos or sequences of images, we recomend using glslUniforms node, so it's better cached and optimized, buy preventing changing loading all the frames everytime you edit your code.
    # """

    def main(self, **kwargs):
        context = Context()

        index = 0
        total = len(kwargs.items())
        pbar = comfy.utils.ProgressBar( total )
        for key, value in kwargs.items():
            # Update Progress Bar
            if comfy.utils.PROGRESS_BAR_ENABLED:
                pbar.update_absolute(index + 1, total)

            if key.startswith("u_tex"):
                context.loadTexture(key, value)
                
            elif key.startswith("u_val"):
                context.setUniform(key, value)

            index += 1
        
        return (context, )
