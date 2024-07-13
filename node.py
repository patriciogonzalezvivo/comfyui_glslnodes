class GlslNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "fragment_shader": "STRING",
            }
        }
    CATEGORY = "GlslNode"
    FUNCTION = "main"
    RETURN_TYPES = ("IMAGE", )

    def main(self, fragment_shader):
        
        return 