import moderngl
from PIL import Image

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
        data = self.fbo.read(components=4)
        return Image.frombytes("RGBA", self.fbo.size, data)


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
        data = self.fbos[self.index].read(components=4)
        return Image.frombytes("RGBA", self.fbos[self.index].size, data)