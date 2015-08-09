# EdisonILI9341
Library for Intel Edison and ILI9341 SPI Screen

Allows Edison to drive the ILI9341 display screen using python and intel's mraa library. 

This library has a few dependencies. Installation instructions below.

1. Intel's mraa library - Install with 

$ echo "src mraa-upm http://iotdk.intel.com/repos/1.1/intelgalactic" > /etc/opkg/mraa-upm.conf
$ opkg update
$ opkg install libmraa0

2. NumPy

Install by sourcing alex T's repos. Instructions here: http://alextgalileo.altervista.org/edison-package-repo-configuration-instructions.html 

Then installing numpy

$ opkg update
$ opkg install python-numpy

Two examples are provided for using the library:

1. example_shapes.py - Example of how to draw shapes on a red background and render them to the screen. 

2. photo.py - Example of how to load a photo, resize and rotate it, and render it to the screen. 

