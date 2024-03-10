#!/usr/bin/env python3
##################################################
# Paint Drips

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
s.clear()
V0 = s.get_pixels()
V1 = V0

# Setup parameters:

# Fade out coefficient
Fade :float =0.3
# DripProbability: if random 0-100% is less than this value then drip
DripProb :int =30
# Minimum Pixel R,G,B lightness for random generation:
MinLight :int =200
# Delay time between each cycle
CycleDelay :float =0.15
# Inherit Neighbour's value by this ratio
# Take this ratio from neighbour's color and the remaining from self
# For example : 0.1
# Left, right, top, bottom pixels values are taken by 0.1-0.1 each,
# and then self's previous color by 0.6
InheritNeighbour :float =0.6

# Don't setup this, it will be calculated:
InheritSelf :float =1.0


def clamp(_val :int) -> int :
    return max(min(_val,255),0)


while True:

    for j in range(8) :
        for i in range(8) :
            curridx = j*8+i

            # Assume that inherit full ratio from self.
            # R0,G0,B0 is self's current color, R1,G1,B1 is self's next color
            #InheritSelf = 1.0
            R0,G0,B0 = V0[curridx]
            R1,G1,B1 = (0,0,0)

            # Check in each directions if neighbour pixel is still on the 8x8 map
            # If success, take out the neighbour's ratio from self's ratio
            for (di,dj) in ((-1,0), (1,0), (0,-1), (0,1)) :
                if ((i+di) in range(8)) and ((j+dj) in range(8)) :
                    Rx,Gx,Bx = V0[(j+dj)*8+i+di]
                    R1 += round(Rx*InheritNeighbour)
                    G1 += round(Gx*InheritNeighbour)
                    B1 += round(Bx*InheritNeighbour)
                    #InheritSelf = InheritSelf - InheritNeighbour

            # Take the previous self pixel with the remaining ratio
            R1 += round(R0*InheritSelf)
            G1 += round(G0*InheritSelf)
            B1 += round(B0*InheritSelf)

            # Finally let it fade with the desired value
            R1 = clamp(round(R1*Fade))
            G1 = clamp(round(G1*Fade))
            B1 = clamp(round(B1*Fade))

            # Copy back the new value to the new vector
            V1[curridx] = list((R1,G1,B1))


    # If the drip probability hits , make a drip somewhere
    if r(0,100) <= DripProb :
        # Lightness generated first
        L=r(MinLight,255)
        # Actual color is a number triplet, R,G,B value all equal L first
        C=list((L,L,L))
        # think of an index out of the 3, then an other index that differs
        p=r(0,2) ; q=p
        while q == p : q = r(0,2)
        # Now one of R,G,B gets low, the other gets halved
        C[q]=round(L/6.0)
        C[p]=round(L/2.0)

        ri = r(0,7) ; rj = r(0,7) ; curridx = rj*8+ri
        for (di,dj) in ((-1,0), (1,0), (0,-1), (0,1)) :
            if ((ri+di) in range(8)) and ((rj+dj) in range(8)) :
                V1[(rj+dj)*8+ri+di] = C
        V1[curridx] = C

    # Now draw the new vector and make it the old vector
    s.set_pixels(V1)
    V0 = V1
    sleep(CycleDelay)

