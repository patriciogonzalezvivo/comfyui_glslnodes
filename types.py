class GlslInt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("INT", { "default": 0.0 }),
            }
        }
    
    CATEGORY = "GLSL"
    FUNCTION = "main"

    RETURN_TYPES = ("INT", )
    RETURN_NAMES = ("int", )

    def main(self, value):
        return (value, )
    

class GlslFloat:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("FLOAT", { "default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001 }),
            }
        }
    
    CATEGORY = "GLSL"
    FUNCTION = "main"

    RETURN_TYPES = ("FLOAT", )
    RETURN_NAMES = ("float", )

    def main(self, value):
        return (value, )
    

class GlslVec2:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "x": ("FLOAT", { "default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001 }),
                "y": ("FLOAT", { "default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001 }),
            }
        }
    
    CATEGORY = "GLSL"
    FUNCTION = "main"

    RETURN_TYPES = ("VEC2", )
    RETURN_NAMES = ("vec2", )

    def main(self, x, y):
        return ((x, y), )


class GlslVec3:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "x": ("FLOAT", { "default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001 }),
                "y": ("FLOAT", { "default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001 }),
                "z": ("FLOAT", { "default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001 }),
            }
        }
    
    CATEGORY = "GLSL"
    FUNCTION = "main"

    RETURN_TYPES = ("VEC3", )
    RETURN_NAMES = ("vec3", )

    def main(self, x, y, z):
        return ((x, y, z), )


class GlslVec4:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "x": ("FLOAT", { "default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001 }),
                "y": ("FLOAT", { "default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001 }),
                "z": ("FLOAT", { "default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001 }),
                "w": ("FLOAT", { "default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001 }),
            }
        }
    
    CATEGORY = "GLSL"
    FUNCTION = "main"

    RETURN_TYPES = ("VEC4", )
    RETURN_NAMES = ("vec3", )

    def main(self, x, y, z, w):
        return ((x, y, z,w), )