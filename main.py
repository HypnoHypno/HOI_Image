import argparse
import numpy
import binascii
from PIL import Image, ImageColor

# Errors
class HeaderError(Exception):
    __module__ = Exception.__module__
    MALFORMEDSIZE = "Malformed Image size, please ensure your file isn't corrupted."
    MALFORMEDCOMP = "Malformed Compression byte, please ensure your file isn't corrupted."

# Other Classes
class Version:
    LATEST = 2

class SafeHex:
    def __init__(self, number=0):
        self.RESULT = "{:0x}".format(number)

class Input:
    IMAGE, WIDTH, HEIGHT, TYPE = (None, None, None, None)
    def __init__(self, file="input.jpg", mode=0, version=Version.LATEST):
        if mode == 0:
            self.IMAGE = Image.open(file).convert('RGBA')
            self.WIDTH, self.HEIGHT = self.IMAGE.size
            self.TYPE = "normal"
            return
        self.TYPE = "hoi"
        
        with open(file, "rb") as f:
            self.IMAGE = f.read()
        self.IMAGE = self.IMAGE.hex()
        
        aftersignature = self.IMAGE[len(Header.SIGNATURE_HEX[str(version-1)]):]
        
        size = self.GetHoiSize(aftersignature) # Tuple: (width or height, everything after size is specified)
        
        if ( aftersignature[0] == "d" ):
            self.WIDTH = int(size[0])
        elif ( aftersignature[0] == "e" ):
            self.HEIGHT = int(size[0]) 
        else:
            raise HeaderError(HeaderError.MALFORMEDSIZE)
        
        self.IMAGE = size[1] # This is everything after the size is specified in byte based format.
        
        if ( version > 1 ):
            comp = self.IMAGE[:2]
            self.IMAGE = self.IMAGE[2:]
            if ( comp == "ff" ): # This image is compressed, we should unpack it.
                i = 0
                uncompressed = []
                while i < len(self.IMAGE):
                    try:
                        value = self.IMAGE[i:i+4]
                        repeat = int(self.IMAGE[i+4:i+6], 16) + 1
                        uncompressed.append(value * repeat)
                        i += 6
                    except:
                        break
                self.IMAGE = ''.join(uncompressed)
            elif ( not comp == "00" ):
                raise HeaderError(HeaderError.MALFORMEDCOMP)
        
        lenbytes = int(len(self.IMAGE) / 4) # 2 bytes are used per pixel, which is 4 bits in hex.
        
        if ( aftersignature[0] == "d" ): # If you get the total amount of pixels in an image and divide it by either the width or height, you will get the other metric in the image.
            self.HEIGHT = int(lenbytes / self.WIDTH)
        else:
            self.WIDTH = int(lenbytes / self.HEIGHT)
    
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
        data = self.IMAGE.getdata()
        rgba_map = numpy.array(Palette.RGBA_Map)
        outhex = []
        outrgba = []
        
        for px in data:
            for color in px:
                difference_array = numpy.absolute(rgba_map-color)
                index = difference_array.argmin()
                outhex.append(Palette.BYTE_Map[index])
                outrgba.append(Palette.RGBA_Map[index])
        
        outhex = "".join(outhex)
        
        while not len(outhex) % 2 == 0:
            outhex += "0"
        
        return (outhex, outrgba)
    
    def ScanColorHoi(self, target):
        data = self.IMAGE
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

class Header:
    SIGNATURE_HEX = {
        "1": "484F495F3100", # HOI_1[null]
        "2": "484F495F3200"  # HOI_2[null]
    }
    SIGNATURE_BYTES = {
        "1": b'HOI_1\x00',
        "2": b'HOI_2\x00'
    }
    def __init__(self, width=1280, height=720, version=2, compression=True):
        def Width(width):
            out = "D" + str(width) + "D"
            return out + "0" if not len(out) % 2 == 0 else out
        
        def Height(height):
            out = "E" + str(height) + "E"
            return out + "0" if not len(out) % 2 == 0 else out
        
        width = Width(width)
        height = Height(height)
        self.CONTENT = self.SIGNATURE_HEX[str(version)] + width if len(width) <= len(height) else height
        self.CONTENT += "FF" if compression else "00"
    
    def SignatureMatch(self, file):
        with open(file, "rb") as f:
            read = f.read(6)
            bytes = self.SIGNATURE_BYTES.values()
            r1 = ( read in bytes )
            try:
                r2 = list(bytes).index(read)
            except:
                r2 = None
            return (r1, r2)

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
    
    def GetImageData(self):
        return self.image_data

    def GetHeader(self):
        return self.header
    
    def CompressImageData(self):
        # Convert hex string to a numpy array of integers
        image_array = numpy.array([int(self.image_data[i:i+4], 16) for i in range(0, len(self.image_data), 4)], dtype=numpy.uint16)
            
        compressed = ""
        index = 0
        
        while index < len(image_array):
            current_pixel = image_array[index]
        
            # Count the number of consecutive pixels that are the same
            repeat = 0
            while repeat < 255 and index + repeat + 1 < len(image_array) and image_array[index + repeat + 1] == current_pixel:
                repeat += 1
            
            # Append the compressed pixel to the result
            compressed += format(current_pixel, '04x') + format(repeat, '02x')
            
            # Move the index to the next pixel
            index += repeat + 1
        
        return compressed
    
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

# Main functionality
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, default='input.jpg')
    args = parser.parse_args()
    
    signaturematch = Header().SignatureMatch(file=args.input)
    
    mode = 1 if signaturematch[0] else 0
    
    if signaturematch[0]:
        hoiversion = signaturematch[1] + 1
    
    if mode == 0: # Convert to .hoi
        out = Output()
        image = Input(args.input)
        out.SetImageData(image.ScanColor()[0])
        compresseddata = out.CompressImageData()
        compressedbool = (len(compresseddata) <= len(out.GetImageData()))
        if compressedbool:
            out.SetImageData(compresseddata)
        header = Header(width=image.WIDTH, height=image.HEIGHT, compression=compressedbool)
        out.SetHeader(header)
        out = out.Compile()
        ext = args.input.split('.')[0] + ".hoi"
        with open(ext, "wb") as f:
            f.write(out)
    else: # Convert .hoi to .png
        image = Input(args.input, mode=1, version=hoiversion)
        out = Image.new('RGBA', (image.WIDTH, image.HEIGHT), (0, 0, 0, 0))
        image.ScanColor(out) # Works differently on .hoi files, you specify a target image and it'll draw every pixel on it.
        out.save(args.input + ".png")
        out.show()
