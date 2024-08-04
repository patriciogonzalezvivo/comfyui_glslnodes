import moderngl
from PIL import Image
import numpy as np

class ImageTexture:
    def __init__(self, image, name : str = None, ctx=None):
        self.name = name
        if ctx is None:
            self.ctx = moderngl.get_context()
        else:
            self.ctx = ctx

        print(name, image.shape)
        self.width = image.shape[1]
        self.height = image.shape[0]

        if len(image.shape) == 2:
            print(name, "is a MASK")
            self.channels = 3

            tmp = np.zeros( ( image.shape[0], image.shape[1], 3 ) )
            tmp[:,:,0] = image
            tmp[:,:,1] = image
            tmp[:,:,2] = image

            # If the snowy library is installed, generate a signed distance field from the mask
            try:
                import snowy
                mask = snowy.rgb_to_luminance( snowy.extract_rgb(tmp) )
                dist = snowy.generate_sdf(mask != 0.0)
                dist = dist / 255.0
                tmp[:,:,1] = np.clip(dist[...,0], 0.0, 1.0)
                tmp[:,:,2] = 1.0+np.clip(dist[...,0], -1.0, 0.0)

            except ModuleNotFoundError:
                print("snowy is not installed")

            image = tmp
            
        elif image.shape[2] == 2:
            print(name, "is a FLOW")
            self.channels = 3

            # FLOW should be more that one image but just in case
            # TODO: ...

        else:
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


class ImageArrayTexture:
    def __init__(self, imageList, name:str = None, ctx=None):
        self.name = name
        if ctx is None:
            self.ctx = moderngl.get_context()
        else:
            self.ctx = ctx

        self.width = imageList[0].shape[1]
        self.height = imageList[0].shape[0]

        if len(imageList[0].shape) == 2:
            print(name, "is a MASK")
            self.channels = 3

            tmpList = []
            for image in imageList:
                tmp = np.zeros( ( image.shape[0], image.shape[1], 3 ) )
                tmp[:,:,0] = image
                tmp[:,:,1] = image
                tmp[:,:,2] = image

                # If the snowy library is installed, generate a signed distance field from the mask
                try:
                    import snowy
                    mask = snowy.rgb_to_luminance( snowy.extract_rgb(tmp) )
                    dist = snowy.generate_sdf(mask != 0.0)
                    dist = dist / 255.0
                    tmp[:,:,1] = np.clip(dist[...,0], 0.0, 1.0)
                    tmp[:,:,2] = 1.0+np.clip(dist[...,0], -1.0, 0.0)

                except ModuleNotFoundError:
                    print("snowy is not installed")

                tmpList.append(tmp)
            
            imageList = tmpList
            
        elif imageList[0].shape[2] == 2:
            print(name, "is a FLOW")
            self.channels = 3

            # FLOW videos have one less frame that original. First one is empty
            tmpList = [ np.zeros( ( imageList[0].shape[0], imageList[0].shape[1], 3 ) ) * 0.5 + 0.5 ]

            for image in imageList:
                tmp = np.zeros( ( image.shape[0], image.shape[1], 3 ) )
                tmp[:,:,0] = np.clip( (image[:,:,0] / 255.0) * 0.5 + 0.5, 0.0, 1.0)
                tmp[:,:,1] = np.clip( (image[:,:,1] / 255.0) * 0.5 + 0.5, 0.0, 1.0)
                tmp[:,:,2] = 0.0
                tmpList.append(tmp)
            
            imageList = tmpList

        else:
            self.channels = imageList[0].shape[2]
            
        self.totalFrames = len(imageList)

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


    def use(self, index:int, program:moderngl.Program = None):
        if program is not None:
            if self.name in program:
                program[self.name] = index

            if f"{self.name}Resolution" in program:
                program[f"{self.name}Resolution"] = (float(self.width), float(self.height))

            if f"{self.name}TotalFrames" in program:
                program[f"{self.name}TotalFrames"] = self.totalFrames

        self.texture.use(location=index)
        self.sampler.use(location=index)