#!/usr/bin/env python3
####################################################
# Starry Night 1

from random import randint as r
from time import sleep
try :
    from sense_hat import SenseHat
except :
    try :
        from sense_emu import SenseHat
    except :
        from _sense_hat_ANSI import SenseHat

s=SenseHat()
s.clear([0,0,48])

while True:
    if r(0,100) > 90 :
        # Draw a shiny star
        s.set_pixel(r(0,7), r(0,7), list((r(80,255), r(80,255), r(80,255))))
    else :
        # Draw a flickery bgr
        s.set_pixel(r(0,7), r(0,7), list((0, 0, r(48,150))))
    sleep(0.1)
