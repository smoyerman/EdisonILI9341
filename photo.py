""" Showing a picture """

import Image

# Load the image
image = Image.open('gray.png')

# Resize the image and rotate it so it's 240x320 pixels.
image = image.rotate(90).resize((240, 320))

# Draw the image on the display hardware.
disp.display(image)
