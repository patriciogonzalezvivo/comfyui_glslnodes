from .glsl_utils import resolveLygia, GLSL_VERSIONS, DEFAULT_FRAGMENT_SHADER, DEFAULT_SHADERTOY_SHADER


class GlslShaderToy:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "code": ("STRING", {"multiline": True, "default": DEFAULT_SHADERTOY_SHADER}),
            },
        }
    CATEGORY = "GLSL"
    FUNCTION = "main"
    RETURN_TYPES = ("GLSL_CODE", )

    def main(self, code):
        out = {}
        out["version"] = "440"
        out["type"] = "fragment"
        out["src"] = resolveLygia(code)
        out["specs"] = "shadertoy"
        return (out, )


class GlslEditor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "version" : (GLSL_VERSIONS, {"default": "130" }),
                "code": ("STRING", {"multiline": True, "default": DEFAULT_FRAGMENT_SHADER}),
                "type": (["fragment"], { "default": "fragment" }),
            },
        }
    CATEGORY = "GLSL"
    FUNCTION = "main"
    RETURN_TYPES = ("GLSL_CODE", )

    def main(self, version, type, code):
        out = {}
        out["version"] = version
        out["type"] = type
        out["src"] = resolveLygia(code)
        out["specs"] = "raw"
        return (out, )
    

class GlslEditorIde:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "version" : (GLSL_VERSIONS, {"default": "130" }),
                "type": (["fragment"], { "default": "fragment" }),
                "code": ("GLSL_STRING", {"default": DEFAULT_FRAGMENT_SHADER}),
            },
        }
    CATEGORY = "GLSL"
    FUNCTION = "main"
    RETURN_TYPES = ("GLSL_CODE", )

    def main(self, **kwargs):
        out = {}
        out["version"] = kwargs["version"]
        out["type"] = kwargs["type"]
        out["src"] = resolveLygia( kwargs["code"] )
        out["specs"] = "raw"
        return (out, )