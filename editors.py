from .utils import resolveLygia, GLSL_VERSIONS, DEFAULT_FRAGMENT_SHADER, DEFAULT_SHADERTOY_SHADER


class GlslShaderToy:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "glsl_code": ("STRING", {"multiline": True, "default": DEFAULT_SHADERTOY_SHADER}),
            },
        }
    CATEGORY = "GLSL"
    FUNCTION = "main"
    RETURN_TYPES = ("GLSL_CODE", )

    def main(self, glsl_code):
        out = {}
        out["version"] = "440"
        out["src"] = resolveLygia(glsl_code)
        out["specs"] = "shadertoy"
        return (out, )


class GlslEditor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "glsl_version" : (GLSL_VERSIONS, {"default": "130" }),
                "glsl_code": ("STRING", {"multiline": True, "default": DEFAULT_FRAGMENT_SHADER}),
            },
        }
    CATEGORY = "GLSL"
    FUNCTION = "main"
    RETURN_TYPES = ("GLSL_CODE", )

    def main(self, glsl_version, glsl_code):
        out = {}
        out["version"] = glsl_version
        out["src"] = resolveLygia(glsl_code)
        out["specs"] = "raw"
        return (out, )