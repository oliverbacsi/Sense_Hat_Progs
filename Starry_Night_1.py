#!/usr/bin/env python3
####################################################
# Starry Night 1

import sense_hat
from random import randint as r
from time import sleep

s=sense_hat.SenseHat()
s.clear((0,0,48))

while True:
    if r(0,100) > 90 :
        # Draw a shiny star
        s.set_pixel(r(0,7), r(0,7), r(80,255), r(80,255), r(80,255))
    else :
        # Draw a flickery bgr
        s.set_pixel(r(0,7), r(0,7), 0, 0, r(48,150))
    sleep(0.1)
