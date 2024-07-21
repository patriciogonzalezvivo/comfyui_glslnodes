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

    RETURN_TYPES = ("GLSL_CONTEXT",)
    RETURN_NAMES = ("uniforms",)

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
                context.setTexture(key, value)
                
            elif key.startswith("u_val"):
                context.setUniform(key, value)

            index += 1
        
        return (context, )
