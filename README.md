# HOI
Stands for Hex Operating Image Format.

Inspired by face-hh's "[bruh](https://github.com/face-hh/bruh)" format, I'm coding together a python-based image format which uses a byte-based format, as opposed to a dump of hex colors.

![Example Image](/output.png)

This is an example image of 1 MB in size, made from converting a photo to HOI V1 and back to PNG. You can view the original [here](https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png).

The color-banding is due to a palette of 4096 colors being superimposed onto the image due to byte limits.

Color-banding, accuracy, and size should improve as code is in the works to add a palette feature to HOI rather than forcing a set palette, and to add compression when pixels repeat, specifically.

# How to use:
1. Download this repo by [github.com/HypnoHypno/HOI_Image/zipball/master](clicking this link).
2. Run "main.py" with the path to your input image as an argument. (HOI or any other format to convert to HOI.)
3. Wait until the conversion is done, this can take a few minutes if your image is large, but should take around half a minute.

Alternatively, you can also drag a file into "main.exe" to use the last stable version of HOI if you aren't risk averse to that sort of thing, or compile main.py yourself.

When using a .exe version, you should set the default program for HOI files to your .exe file by:
1. Right clicking on a HOI file.
2. Hovering over "Open with".
3. Clicking "Choose another app", checking "Always use this app", and clicking "More apps".
4. Scrolling to the bottom, where you'll see "Look for another app on this PC", clicking it and navigating to your exe file.
5. Double clicking the .exe file.
6. You're done!

!["Open with" panel](/open_with_panel.png)
