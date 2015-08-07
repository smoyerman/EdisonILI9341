""" Showing a picture """
import Image
import ILI9341

disp = ILI9341.ILI9341()
disp.begin()

# Load the image
image = Image.open('/home/root/BlueFrog_processed.jpg')

# Resize the image and rotate it so it's 240x320 pixels.
image = image.rotate(90).resize((240, 320))

# Draw the image on the display hardware.
disp.display(image)
