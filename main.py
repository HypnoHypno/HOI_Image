import argparse
import numpy
import binascii
from PIL import Image, ImageColor

# Errors
class HeaderError(Exception):
    __module__ = Exception.__module__
    MALFORMEDSIZE = "Malformed Image size, please ensure your file isn't corrupted."

# Other Classes
class SafeHex:
    def __init__(self, number=0):
        self.RESULT = "{:0x}".format(number)
        return

class Input:
    IMAGE, WIDTH, HEIGHT, TYPE = (None, None, None, None)
    def __init__(self, file="input.jpg", mode=0):
        if mode == 0:
            self.IMAGE = Image.open(file).convert('RGBA')
            self.WIDTH, self.HEIGHT = self.IMAGE.size
            self.TYPE = "normal"
            return
        self.TYPE = "hoi"
        
        with open(file, "rb") as f:
            self.IMAGE = f.read()
        self.IMAGE = self.IMAGE.hex()
        
        aftersignature = self.IMAGE[len(Header.SIGNATURE_HEX):]
        
        size = self.GetHoiSize(aftersignature) # Tuple: (width or height, everything after size is specified)
        
        if ( aftersignature[0] == "d" ):
            self.WIDTH = int(size[0])
        elif ( aftersignature[0] == "e" ):
            self.HEIGHT = int(size[0]) 
        else:
            raise HeaderError(HeaderError.MALFORMEDSIZE)
        
        self.IMAGE = size[1] # This is everything after the size is specified in byte based format.
        databytes = int(len(self.IMAGE) / 4) # 2 bytes are used per pixel, which is 4 bits in hex.
        
        if ( aftersignature[0] == "d" ): # If you get the total amount of pixels in an image and divide it by either the width or height, you will get the other metric in the image.
            self.HEIGHT = int(databytes / self.WIDTH)
        else:
            self.WIDTH = int(databytes / self.HEIGHT)
    
    def GetHoiSize(self, aftersignature):
        """
        Image size is stored like this:
        "D1 28 0D" means width is 1280.
        "E7 20 E0" means height is 720.
        
        We can infer width from height and
        vice versa using how many bytes there
        are, so it's pointless to store both.
        """
        size = ""
        aftersignature = aftersignature[1:] # Ignore the first character specifying if we're working with width or height.
        for i in aftersignature:
            aftersignature = aftersignature[1:] # Remove this character from aftersignature, so we can return everything after the size is specified along with the size.
            try:
                int(i)
            except:
                break # Break once we've hit a character, rather than a number.
            size += i
        try:
            int(size)
        except:
            raise HeaderError(HeaderError.MALFORMEDSIZE)
        while not len(aftersignature) % 2 == 0:
            aftersignature = aftersignature[1:] # When dealing with a size that has an odd number of bytes (Example: 720 in 1280x720) you add hex bits of 0 the values
            # Like E7 20 E0. This code is to filter for that.
        return (size, aftersignature)
    
    def ScanColor(self, target=None):
        return self.ScanColorNormal() if not self.TYPE == "hoi" else self.ScanColorHoi(target)
    
    def ScanColorNormal(self):
        data = list(self.IMAGE.getdata())
        array = numpy.array(Palette.RGBA_Map)
        outhex = ""
        outrgba = []
        for t in data:
            for v in t:
                difference_array = numpy.absolute(array-v)
                index = difference_array.argmin()
                outhex += Palette.BYTE_Map[index]
                outrgba.append(Palette.RGBA_Map[index])
        while not len(outhex) % 2 == 0:
            outhex += "0"
        return (outhex, outrgba)
    
    def ScanColorHoi(self, target):
        data = self.IMAGE
        while not len(data) % 2 == 0:
            data += "0"
        data = [*data]
        p_map = target.load()
        iteration = -1
        for y in range(target.size[1]):
            for x in range(target.size[0]):
                rgba = []
                for v in p_map[x,y]:
                    iteration += 1
                    hex = data[iteration]
                    index = Palette.BYTE_Map.index(hex)
                    rgba.append(Palette.RGBA_Map[index])
                p_map[x,y] = tuple(rgba)
        pass

class Header:
    SIGNATURE_HEX = "484F495F3100" # HOI_1(null) in HEX
    SIGNATURE_BYTES = b'HOI_1\x00'
    def __init__(self, width=1280, height=720):
        def Width(width):
            out = "D" + str(width) + "D"
            return out + "0" if not len(out) % 2 == 0 else out
        
        def Height(height):
            out = "E" + str(height) + "E"
            return out + "0" if not len(out) % 2 == 0 else out
        
        width = Width(width)
        height = Height(height)
        self.CONTENT = self.SIGNATURE_HEX + width if len(width) <= len(height) else height
        return
    
    def SignatureMatch(self, file):
        with open(file, "rb") as f:
            return f.read(6) == self.SIGNATURE_BYTES

class Output:
    header = "00"
    image_data = "00"
    
    def SetHeader(self, header=Header()):
        try:
            self.header = header.CONTENT
        except:
            self.header = header
    
    def SetImageData(self, data):
        try:
            self.image_data = data
        except:
            self.image_data = data[0]
    
    def Compile(self):
        compiled = self.header + self.image_data
        while not len(compiled) % 2 == 0: # Something has gone horribly wrong here. All we can do is add null bits at the end and pray to god that it displays properly.
            compiled += "0"
        compiled = binascii.unhexlify(compiled)
        return compiled

class Palette:
    RGBA_Map = []
    BYTE_Map = []
    pluscount = 1
    for i in range(0,255,16):
        if not i == 0:
            i += pluscount
            pluscount += 1
        RGBA_Map.append(i)
        BYTE_Map.append(SafeHex(pluscount-1).RESULT)
    del pluscount

# Main functionality
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, default='input.jpg')
    args = parser.parse_args()
    
    mode = 1 if Header().SignatureMatch(file=args.input) else 0

    if mode == 0: # Convert to .hoi
        out = Output()
        image = Input(args.input)
        header = Header(image.WIDTH, image.HEIGHT)
        out.SetHeader(header)
        out.SetImageData(image.ScanColor()[0])
        out = out.Compile()
        with open("output.hoi", "wb") as f:
            f.write(out)
    else: # Convert .hoi to .png
        image = Input(args.input, 1)
        out = Image.new('RGBA', (image.WIDTH, image.HEIGHT), (0, 0, 0, 0))
        image.ScanColor(out) # Works differently on .hoi files, you specify a target image and it'll draw every pixel on it.
        out.save("output.png")