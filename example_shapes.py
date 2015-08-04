""" Drawing something """

import ILI9341

disp = ILI9341.ILI9341()
disp.begin()

disp.clear((255, 0, 0))

drawing = disp.draw()

# Draw some shapes.
# Draw a blue ellipse with a green outline.
drawing.ellipse((10, 10, 110, 80), outline=(0,255,0), fill=(0,0,255))

# Draw a purple rectangle with yellow outline.
drawing.rectangle((10, 90, 110, 160), outline=(255,255,0), fill=(255,0,255))

# Draw a white X.
drawing.line((10, 170, 110, 230), fill=(255,255,255))
drawing.line((10, 230, 110, 170), fill=(255,255,255))

# Draw a cyan triangle with a black outline.
drawing.polygon([(10, 275), (110, 240), (110, 310)], outline=(0,0,0), fill=(0,255,255))

disp.display()


