from .glsl_utils import resolveLygia, GLSL_VERSIONS, SHADER_TYPES, DEFAULT_FRAGMENT_SHADER, DEFAULT_SHADERTOY_SHADER


class GlslEditor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "version" : (GLSL_VERSIONS, {"default": "130" }),
                "code": ("STRING", {"multiline": True, "default": DEFAULT_FRAGMENT_SHADER}),
                "type": (SHADER_TYPES, { "default": "fragment" }),
            },
        }
    CATEGORY = "GLSL"
    FUNCTION = "main"
    RETURN_TYPES = ("GLSL_CODE", )

    def main(self, version, type, code):
        out = {}

        if type == "fragment (shadertoy)":
            out["version"] = "440"
            out["type"] = "fragment"
            out["src"] = resolveLygia(code)
            out["specs"] = "shadertoy"
            return (out, )
        else:
            out["version"] = version
            out["type"] = type
            out["src"] = resolveLygia(code)
            out["specs"] = "raw"
            return (out, )
    

class GlslEditorPro:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "version" : (GLSL_VERSIONS, {"default": "130" }),
                "type": (SHADER_TYPES, { "default": "fragment" }),
                "code": ("GLSL_STRING", {"default": DEFAULT_FRAGMENT_SHADER}),
            },
        }
    CATEGORY = "GLSL"
    FUNCTION = "main"
    RETURN_TYPES = ("GLSL_CODE", )

    def main(self, version, type, code):
        out = {}

        if type == "fragment (shadertoy)":
            out["version"] = "440"
            out["type"] = "fragment"
            out["src"] = resolveLygia(code)
            out["specs"] = "shadertoy"
            return (out, )
        else:
            out["version"] = version
            out["type"] = type
            out["src"] = resolveLygia(code)
            out["specs"] = "raw"
            return (out, )