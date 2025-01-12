from .glsl_utils import resolveLygia, resolveLocalIncludes, GLSL_VERSIONS, SHADER_TYPES, DEFAULT_FRAGMENT_SHADER, DEFAULT_SHADERTOY_SHADER




class GlslEditor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "version" : (GLSL_VERSIONS, {"default": "140" }),
                "type": (SHADER_TYPES, { "default": "fragment" }),
                "code": ("STRING", {"multiline": True, "default": DEFAULT_FRAGMENT_SHADER}),
                "local_include": ("BOOLEAN", {"default": False}),
                "include_root": ("STRING", {"default": "", "multiline": False}),
            },
        }
    CATEGORY = "GLSL"
    FUNCTION = "main"
    RETURN_TYPES = ("GLSL_CODE", )
    DESCRIPTION = """
    This node is a simple GLSL editor.
    You can choose your GLSL version. Watch out, not all drivers support all versions: Ex. 130, 420, 430 and 440 are not supported in macOS.
    In types for the moment we only support fragment shaders. "fragment (ShaderToy)" creates wrappes so it follows the ShaderToy specs.
    """

    def main(self, version:str, type:str, code:str, local_includes:bool, include_root:str):
        out = {}

        if type == "fragment (shadertoy)":
            out["version"] = "400"
            out["type"] = "fragment"
            out["src"] = resolveLocalIncludes(code, include_root) if local_includes else resolveLygia(code)
            out["specs"] = "shadertoy"
            return (out, )
        else:
            out["version"] = version
            out["type"] = type
            out["src"] = resolveLocalIncludes(code, include_root) if local_includes else resolveLygia(code)
            out["specs"] = "raw"
            return (out, )
    

class GlslEditorPro:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "version" : (GLSL_VERSIONS, {"default": "140" }),
                "type": (SHADER_TYPES, { "default": "fragment" }),
                "code": ("GLSL_STRING", {"default": DEFAULT_FRAGMENT_SHADER}),
                "local_includes": ("BOOLEAN", {"default": False}),
                "include_root": ("STRING", {"default": "", "multiline": False}),
            },
        }
    CATEGORY = "GLSL"
    FUNCTION = "main"
    RETURN_TYPES = ("GLSL_CODE", )
    # DESCRIPTION = """
    # This node is a GLSL editor with a better interface.
    # You can choose your GLSL version. Watch out, not all drivers support all versions: Ex. 130, 420, 430 and 440 are not supported in macOS.
    # In types for the moment we only support fragment shaders. "fragment (ShaderToy)" creates wrappes so it follows the ShaderToy specs.
    # """

    def main(self, version:str, type:str, code:str, local_includes:bool, include_root:str):
        out = {}

        if type == "fragment (shadertoy)":
            out["version"] = "400"
            out["type"] = "fragment"
            out["src"] = resolveLocalIncludes(code, include_root) if local_includes else resolveLygia(code)
            out["specs"] = "shadertoy"
            return (out, )
        else:
            out["version"] = version
            out["type"] = type
            out["src"] = resolveLocalIncludes(code, include_root) if local_includes else resolveLygia(code)
            out["specs"] = "raw"
            return (out, )