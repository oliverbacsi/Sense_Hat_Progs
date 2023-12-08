#!/usr/bin/env python3
########################################
# Fire emulator
#

import random, time
try :
    from sense_hat import SenseHat
except :
    try :
        from sense_emu import SenseHat
    except :
        from _sense_hat_ANSI import SenseHat

# NUMBER OF FIRE CORES IN EACH STEP
Core :int =2

# FIRE HEAT AT THE CORE
Heat :int =1000

# FADE AWAY COEFFICIENT
Fade :float =0.175


# Initialize
b = [0]*73
s = SenseHat()
s.clear ()
V = s.get_pixels()


def getColor(_val :int) -> list :
    """Determine the pixel color for a value.
    Parameters:
    :param _val : The value of the pixel in the database as int.
    :returns : RGB color triplet as a list:"""
    Rx = min(max(int(_val*1.75),0),255)
    Gx = min(max(int((_val-60)*3.0),0),255)
    return [Rx,Gx,0]


while True:
    for i in range(64,72) : b[i]=0
    for i in range(Core) : b[random.randint(64,71)]=Heat
    for i in range(64) :
        b[i]=int((2*b[i]+b[i+1]+b[i+8]+b[i+9])*Fade)
        V[i]=getColor(b[i])
    s.set_pixels(V)
    time.sleep(0.1)
