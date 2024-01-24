# HOI
Stands for Hex Operating Image Format.

Inspired by face-hh's "[bruh](https://github.com/face-hh/bruh)" format, I'm coding together a python-based image format which uses a byte-based format, as opposed to a dump of hex colors.

![Example Image](/documentation/output.png)

This is an example image of 1 MB in size, made from converting a photo to HOI V1 and back to PNG. You can view the original [here](https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png).

The color-banding is due to a palette of 4096 colors being superimposed onto the image due to byte limits.

Color-banding, accuracy, and size should improve as code is in the works to add a palette feature to HOI rather than forcing a set palette, and to add compression when pixels repeat, specifically.

# How to use:
1. Download this repo by [clicking this link](github.com/HypnoHypno/hoi/zipball/master).
2. Run "main.py" with the path to your input image as an argument. (HOI or any other format to convert to HOI.)
3. Wait until the conversion is done, this can take a few minutes if your image is large, but should take around half a minute.

Alternatively, you can also drag a file into the executable file in "main.rar" to use the last stable version of HOI if you aren't risk averse to that sort of thing, or compile main.py yourself.

When using a .exe version, you should set the default program for HOI files to your .exe file by:
1. Right clicking on a HOI file.
2. Hovering over "Open with".
3. Clicking "Choose another app", checking "Always use this app", and clicking "More apps".
4. Scrolling to the bottom, where you'll see "Look for another app on this PC", clicking it and navigating to your exe file.
5. Double clicking the .exe file.
6. You're done!

!["Open with" panel](/documentation/open_with_panel.png)

# Issues:
1. The HOI file is too big compared to other file formats.

   This is due to the lack of compression, each pixel in the image is encoded as 2 bytes. Be patient! A compression system will be implemented in the next version, HOI_2.

2. There's color banding, and colors can sometimes be slightly off.

   This is due to the fact that there are only 16 different variations of each Red, Green, and Blue value, as opposed to the 256 variations.
   This causes there to be 16^3 (4096) unique colors to use, which can get close to the original colors, but nearly never 100% accurate.

   A fix for this will be made, in the form of having the 16 different activations be variable, and change depending on what is best for the image being encoded.
   The activations will be added to the HOI file, allowing more accurate colors, and (hopefully) less color banding.

3. Conversion to and from HOI takes a few seconds.

   This is because conversion iterates over every pixel in the image, which can take some time.
   On extremely large images, converting to and from HOI can take over 20 seconds, however it usually takes 1-5 seconds on lower sized images.

   This is low priority at the moment.
