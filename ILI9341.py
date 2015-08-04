import mraa as m
import Image
import time
import ImageDraw
import numpy as np
import os

# Constants for interacting with display registers.
ILI9341_TFTWIDTH    = 240
ILI9341_TFTHEIGHT   = 320

ILI9341_NOP         = 0x00
ILI9341_SWRESET     = 0x01
ILI9341_RDDID       = 0x04
ILI9341_RDDST       = 0x09

ILI9341_SLPIN       = 0x10
ILI9341_SLPOUT      = 0x11
ILI9341_PTLON       = 0x12
ILI9341_NORON       = 0x13

ILI9341_RDMODE      = 0x0A
ILI9341_RDMADCTL    = 0x0B
ILI9341_RDPIXFMT    = 0x0C
ILI9341_RDIMGFMT    = 0x0A
ILI9341_RDSELFDIAG  = 0x0F

ILI9341_INVOFF      = 0x20
ILI9341_INVON       = 0x21
ILI9341_GAMMASET    = 0x26
ILI9341_DISPOFF     = 0x28
ILI9341_DISPON      = 0x29

ILI9341_CASET       = 0x2A
ILI9341_PASET       = 0x2B
ILI9341_RAMWR       = 0x2C
ILI9341_RAMRD       = 0x2E

ILI9341_PTLAR       = 0x30
ILI9341_MADCTL      = 0x36
ILI9341_PIXFMT      = 0x3A

ILI9341_FRMCTR1     = 0xB1
ILI9341_FRMCTR2     = 0xB2
ILI9341_FRMCTR3     = 0xB3
ILI9341_INVCTR      = 0xB4
ILI9341_DFUNCTR     = 0xB6

ILI9341_PWCTR1      = 0xC0
ILI9341_PWCTR2      = 0xC1
ILI9341_PWCTR3      = 0xC2
ILI9341_PWCTR4      = 0xC3
ILI9341_PWCTR5      = 0xC4
ILI9341_VMCTR1      = 0xC5
ILI9341_VMCTR2      = 0xC7

ILI9341_RDID1       = 0xDA
ILI9341_RDID2       = 0xDB
ILI9341_RDID3       = 0xDC
ILI9341_RDID4       = 0xDD

ILI9341_GMCTRP1     = 0xE0
ILI9341_GMCTRN1     = 0xE1

ILI9341_PWCTR6      = 0xFC

ILI9341_BLACK       = 0x0000
ILI9341_BLUE        = 0x001F
ILI9341_RED         = 0xF800
ILI9341_GREEN       = 0x07E0
ILI9341_CYAN        = 0x07FF
ILI9341_MAGENTA     = 0xF81F
ILI9341_YELLOW      = 0xFFE0  
ILI9341_WHITE       = 0xFFFF

os.system("echo on > /sys/devices/pci0000\:00/0000\:00\:07.1/power/control")

# Image to Data - Generator function to convert a PIL image to 16-bit 565 RGB bytes.
def image_to_data(image):
    pb = np.array(image.convert('RGB')).astype('uint16')
    color = ((pb[:,:,0] & 0xF8) << 8) | ((pb[:,:,1] & 0xFC) << 3) | (pb[:,:,2] >> 3)
    return np.dstack(((color >> 8) & 0xFF, color & 0xFF)).flatten().tolist()


# ILI Class 
class ILI9341():

    def __init__(self, width=ILI9341_TFTWIDTH, height=ILI9341_TFTHEIGHT):
        self.dev = m.Spi(5)
        self.dev.frequency(6500000)
        
        # Set SPI GPIO pins
        self.DC_PIN = m.Gpio(9)
        self.DC_PIN.dir(m.DIR_OUT)
        self.DC_PIN.write(1)
        self.width = width
        self.height = height
        
        self.imgbuff = Image.new('RGB', (width, height))

    # Send Command
    def OLEDCommand(self,c):
        a = bytearray(1)
        a[0] = c
        self.DC_PIN.write(0) # DC pin LOW
        out = self.dev.write(a)

    # Send Data
    def OLEDData1(self,c):
        a = bytearray(1)
        a[0] = c
        self.DC_PIN.write(1)	# DC HIGH
        out = self.dev.write(a)

    # Send Data Array
    def OLEDData(self,c):
        block_size = 32
        self.DC_PIN.write(1)	# DC HIGH
        for i in range(0,len(c),block_size):
            out = self.dev.write(bytearray(c[i:i+block_size]))

    # Initialize display
    def begin(self):

        # Initialize the display.
        self.OLEDCommand(0XEF)
        self.OLEDData1(0x03)
        self.OLEDData1(0x80)
        self.OLEDData1(0x02)
        self.OLEDCommand(0XCF)
        self.OLEDData1(0x00)
        self.OLEDData1(0xC1)
        self.OLEDData1(0x30)
        self.OLEDCommand(0XED)
        self.OLEDData1(0x64)
        self.OLEDData1(0x03)
        self.OLEDData1(0x12)
        self.OLEDData1(0x81)
        self.OLEDCommand(0XE8)
        self.OLEDData1(0x85)
        self.OLEDData1(0x00)
        self.OLEDData1(0x78)
        self.OLEDCommand(0XCB)
        self.OLEDData1(0x39)
        self.OLEDData1(0x2C)
        self.OLEDData1(0x00)
        self.OLEDData1(0x34)
        self.OLEDData1(0x02)
        self.OLEDCommand(0XF7)
        self.OLEDData1(0x20)
        self.OLEDCommand(0XEA)
        self.OLEDData1(0x00)
        self.OLEDData1(0x00)
        self.OLEDCommand(ILI9341_PWCTR1)
        self.OLEDData1(0x23)
        self.OLEDCommand(ILI9341_PWCTR2)
        self.OLEDData1(0x10)
        self.OLEDCommand(ILI9341_VMCTR1)
        self.OLEDData1(0x3e)
        self.OLEDData1(0x28)
        self.OLEDCommand(ILI9341_VMCTR2)
        self.OLEDData1(0x86)
        self.OLEDCommand(ILI9341_MADCTL)
        self.OLEDData1(0x48)
        self.OLEDCommand(ILI9341_PIXFMT)
        self.OLEDData1(0x55)
        self.OLEDCommand(ILI9341_FRMCTR1)
        self.OLEDData1(0x00)
        self.OLEDData1(0x18)
        self.OLEDCommand(ILI9341_DFUNCTR)
        self.OLEDData1(0x08)
        self.OLEDData1(0x82)
        self.OLEDData1(0x27)
        self.OLEDCommand(0xF2)
        self.OLEDData1(0x00)
        self.OLEDCommand(ILI9341_GAMMASET)
        self.OLEDData1(0x01)
        self.OLEDCommand(ILI9341_GMCTRP1)
        self.OLEDData1(0x0F)
        self.OLEDData1(0x31)
        self.OLEDData1(0x2B)
        self.OLEDData1(0x0C)
        self.OLEDData1(0x0E)
        self.OLEDData1(0x08)
        self.OLEDData1(0x4E)
        self.OLEDData1(0xF1)
        self.OLEDData1(0x37)
        self.OLEDData1(0x07)
        self.OLEDData1(0x10)
        self.OLEDData1(0x03)
        self.OLEDData1(0x0E)
        self.OLEDData1(0x09)
        self.OLEDData1(0x00)
        self.OLEDCommand(ILI9341_GMCTRN1)
        self.OLEDData1(0x00)
        self.OLEDData1(0x0E)
        self.OLEDData1(0x14)
        self.OLEDData1(0x03)
        self.OLEDData1(0x11)
        self.OLEDData1(0x07)
        self.OLEDData1(0x31)
        self.OLEDData1(0xC1)
        self.OLEDData1(0x48)
        self.OLEDData1(0x08)
        self.OLEDData1(0x0F)
        self.OLEDData1(0x0C)
        self.OLEDData1(0x31)
        self.OLEDData1(0x36)
        self.OLEDData1(0x0F)
        self.OLEDCommand(ILI9341_SLPOUT)
        time.sleep(0.120)
        self.OLEDCommand(ILI9341_DISPON)

    """ Set pixel addresses in window """
    def set_window(self, x0=0, y0=0, x1=None, y1=None):
        # Set Window
        if x1 is None:
            x1 = self.width-1
        if y1 is None:
            y1 = self.height-1
        self.OLEDCommand(ILI9341_CASET)
        self.OLEDData1(x0 >> 8)
        self.OLEDData1(x0 & 0xff)
        self.OLEDData1(x1 >> 8)
        self.OLEDData1(x1 & 0xff)
        self.OLEDCommand(ILI9341_PASET)
        self.OLEDData1(y0 >> 8)
        self.OLEDData1(y0 & 0xff)
        self.OLEDData1(y1 >> 8)
        self.OLEDData1(y1 & 0xff)
        self.OLEDCommand(ILI9341_RAMWR)

    """ Write the display buffer """
    def display(self, image=None):
        if image is None:
            image = self.imgbuff
        # Set address bounds to entire display.
        self.set_window()
        pixelbytes = list(image_to_data(image))
        self.OLEDData(pixelbytes)

    def clear(self, color=(0,0,0)):
        """Clear the image buffer to the specified RGB color (default black)."""
        width, height = self.imgbuff.size
        self.imgbuff.putdata([color]*(width*height))

    def draw(self):
        """Return a PIL ImageDraw instance for 2D drawing on the image buffer."""
        return ImageDraw.Draw(self.imgbuff)


