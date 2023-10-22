#!/usr/bin/env python3
##################################################
# Starry Night 2

import sense_hat
from random import randint as r
from time import sleep

s=sense_hat.SenseHat()
s.clear((0,0,48))
V = s.get_pixels()
Fade :float =0.97

while True:

    # Fade all pixels
    for i in range(64) :
        R,G,B = V[i]
        R=round(Fade*R)
        G=round(Fade*G)
        B=round(Fade*B)
        if R<49 and G<49 and B<49 :
            B = r(48,72)
        V[i] = list((R,G,B))

    # In some percent of the cases
    if r(0,100) > 90 :
        # Draw a shiny star somewhere
        R=r(100,255)
        G=r(100,255)
        B=r(100,255)
        V[r(0,63)] = list((R,G,B))

    s.set_pixels(V)
    sleep(0.1)
