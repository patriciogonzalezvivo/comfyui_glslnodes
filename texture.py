import moderngl
from PIL import Image
import numpy as np

class ImageTexture:
    def __init__(self, image, name = None):
        self.ctx = moderngl.get_context()
        self.name = name

        self.width = image.shape[1]
        self.height = image.shape[0]
        self.channels = image.shape[2]

        image = np.flip(image, 0)
        image = (image * 255).astype(np.uint8)
        self.texture = self.ctx.texture(image.shape[1::-1], self.channels, image)
        self.sampler = self.ctx.sampler(texture=self.texture)
        self.sampler.filter = (self.ctx.NEAREST, self.ctx.NEAREST)

    def use(self, index, program = None):
        self.texture.use(index)
        self.sampler.use(index)

        if program is not None:
            if self.name in program:
                program[self.name] = index

            if f"{self.name}Resolution" in program:
                program[f"{self.name}Resolution"] = (float(self.width), float(self.height))

        index += 1


class ImageArrayTexture:
    def __init__(self, imageList, name = None, defines = None):
        self.ctx = moderngl.get_context()
        self.name = name

        self.width = imageList[0].shape[1]
        self.height = imageList[0].shape[0]
        self.channels = imageList[0].shape[2]
        self.totalFrames = len(imageList)

        if defines is not None:
            defines.append((f"{name.upper()}_TOTALFRAMES", self.totalFrames))

        dataList = []
        for image in imageList:
            image = np.flip(image, 0)
            image = Image.fromarray(np.uint8(image * 255))
            if self.width != image.size[0] or self.height != image.size[1]:
                raise ValueError(f"image size mismatch: {image.size[0]}x{image.size[1]}")
            dataList.append(list(image.getdata()))

        imageArrayData = np.array(dataList, np.uint8)

        self.texture = self.ctx.texture_array((self.width, self.height, self.totalFrames), self.channels, data=imageArrayData)
        # self.texture.build_mipmaps()
        self.texture.filter = (self.ctx.LINEAR, self.ctx.LINEAR)

        self.sampler = self.ctx.sampler(texture=self.texture)
        self.sampler.filter = (self.ctx.LINEAR, self.ctx.LINEAR)

    def use(self, index, program = None):
        if program is not None:
            if self.name in program:
                program[self.name] = range(index, index + self.totalFrames)

            if f"{self.name}Resolution" in program:
                program[f"{self.name}Resolution"] = (float(self.width), float(self.height))

            if f"{self.name}TotalFrames" in program:
                program[f"{self.name}TotalFrames"] = self.totalFrames

        self.texture.use(location=index)
        self.sampler.use(location=index)

        index += 1