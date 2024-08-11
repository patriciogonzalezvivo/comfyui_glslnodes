import moderngl
from PIL import Image

import torch
from torchvision.transforms import PILToTensor
ptt = PILToTensor()

class Buffer:
    def __init__(self, width:int, height:int, name:str=None, ctx=None):
        self.width = width
        self.height = height
        self.name = name
        if ctx is None:
            self.ctx = moderngl.get_context()
        else:
            self.ctx = ctx

        self.fbo = self.ctx.framebuffer(color_attachments=[self.ctx.texture((self.width, self.height), 4)])


    def bind(self):
        self.fbo.use()
        self.ctx.clear(0.0, 0.0, 0.0, 0.0)


    def use(self, index:int, program:moderngl.Program = None):
        self.fbo.color_attachments[0].use(index)
        if program is not None:
            if self.name in program:
                print("Setting", self.name, "to", index)
                program[self.name] = index

            if f"{self.name}Resolution" in program:
                program[f"{self.name}Resolution"] = (float(self.width), float(self.height))


    def getImage(self) -> Image:
        self.fbo.use()
        data = self.fbo.read(components=4)
        return Image.frombytes("RGBA", self.fbo.size, data)
    

    def getTensor(self) -> torch.Tensor:
        image = ptt(self.getImage())
        image = image.permute(1, 2, 0).float().mul(1.0 / 255.0)
        return image.flip(0)


class DoubleBuffer:
    def __init__(self, width:int, height:int, name:str=None, ctx=None):
        self.width = width
        self.height = height
        self.name = name
        if ctx is None:
            self.ctx = moderngl.get_context()
        else:
            self.ctx = ctx

        self.fbos = [   self.ctx.framebuffer(color_attachments=[self.ctx.texture((self.width, self.height), 4)]),
                        self.ctx.framebuffer(color_attachments=[self.ctx.texture((self.width, self.height), 4)])    ]

        self.index = 0


    def bind(self):
        self.index = (self.index + 1) % 2
        self.fbos[self.index].use()
        self.ctx.clear(0.0, 0.0, 0.0, 0.0)


    def use(self, index:int, program:moderngl.Program = None, prev=False):
        i = index
        if prev:
            i = (self.index + 1) % 2
        self.fbos[i].color_attachments[0].use(index)
        if program is not None:
            if self.name in program:
                program[self.name] = index

            if f"{self.name}Resolution" in program:
                program[f"{self.name}Resolution"] = (float(self.width), float(self.height))


    def use(self, index:int, program:moderngl.Program = None):
        self.fbo.color_attachments[0].use(index)
        if program is not None:
            if self.name in program:
                program[self.name] = index

            if f"{self.name}Resolution" in program:
                program[f"{self.name}Resolution"] = (float(self.width), float(self.height))


    def getImage(self) -> Image:
        self.fbos[self.index].use()
        data = self.fbos[self.index].read(components=4)
        return Image.frombytes("RGBA", self.fbos[self.index].size, data)
    

    def getTensor(self) -> torch.Tensor:
        image = ptt(self.getImage())
        image = image.permute(1, 2, 0).float().mul(1.0 / 255.0)
        return image.flip(0)
    

class GlslBuffers:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "buffers" : ("GLSL_BUFFERS", ),
                "type": (["BUFFER", "DOUBLE_BUFFER"], { "default": "BUFFER" }),
                "index": ("INT", {"default": 0}),
            },
        }
    
    CATEGORY = "GLSL"
    FUNCTION = "main"
    RETURN_TYPES = ("IMAGE",)
    DESCRIPTION = """
    This node allows you to extract the content of a buffer or double buffer.
    """

    def main(self, buffers:dict, type:str, index:int, **kwargs):
        if type == "BUFFER":
            # check if the buffer exists, return and empty TENSOR
            if f"u_buffer{index}" not in buffers:
                return torch.zeros(1, 1, 1, 4)
            
            return (buffers[f"u_buffer{index}"], )
        
        elif type == "DOUBLE_BUFFER":
            if f"u_doubleBuffer{index}" not in buffers:
                return torch.zeros(1, 1, 1, 4)
            return (buffers[f"u_doubleBuffer{index}"], )
