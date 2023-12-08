# This file has been written to your home directory for convenience. It is
# saved as "/home/oliver/plumb_line-2023-10-13-17-46-36.py"

from time import sleep
from PIL import Image, ImageDraw
import math
try :
    from sense_hat import SenseHat
except :
    try :
        from sense_emu import SenseHat
    except :
        from _sense_hat_ANSI import SenseHat

hat = SenseHat()

hat.clear()
origin = (7, 7)
while True:
    deg = hat.get_compass()
    # Use the old trick of drawing something too big then down-sizing to get an
    # anti-aliased line
    img = Image.new('RGB', (15, 15))
    draw = ImageDraw.Draw(img)
    dest = (8.0*math.cos(deg*math.pi/180.0), 8.0*math.sin(deg*math.pi/180.0))
    draw.line([origin, dest], fill=(255, 255, 255), width=3)
    img = img.resize((8, 8), Image.BILINEAR)
    hat.set_pixels(list(img.getdata()))
    sleep(0.05)
