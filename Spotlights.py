#!/usr/bin/env python3
##################################################
# Colorful spotlight swiping effect

from random import random as r
from time import sleep
import math

# Initialize the Sense Hat or the Simulator or the lame ANSI replacement
try :
    from sense_hat import SenseHat
except :
    try :
        from sense_emu import SenseHat
    except :
        from _sense_hat_ANSI import SenseHat


# Setup parameters:

# Fade out coefficient : the spotlight fades by this many multiplier
# when going 1 LED distance away from the source
Fade :float =0.6

# Step Angle : An imaginary angle is getting increased by this many radians
# at each screen refresh step. This is the base of the multiplier of each
# coordinate of each color to calculate the sinusoid curve
# the spotlights are moving along.
# Together with the next variable these are specifying the speed of the swiping.
# This is basically the resolution of the movement.
StepAngle :float = 0.01

# Sleep Time : The program is waiting this much time before two screen refreshes
# This is basically the pace of the animation.
SleepTime :float = 0.1

# Check if someone wants to quit
StayInMainLoop :bool = True


# This stores the variables
class Program :
    def __init__(self) :
        self.MainPhase = 2.0 * math.pi * r()
        # Phase multiplier of the sinusoid movement compared to the basic StepAngle
        self.Multiplier :dict = dict(())
        # Current coordinates of the spotlights
        self.Coord :dict = dict(())
        for c in ["R","G","B"] :
            for i in ["X","Y"] :
                self.Multiplier[c+i] = 6.0*r()+0.8
                self.Coord[c+i] = 0.0

    def calc(self) :
        global V, StepAngle, PixList
        # Clear the display list
        V = []
        # First calculate the new positions of the spotlights
        for c in ["R","G","B"] :
            for i in ["X","Y"] :
                self.Coord[c+i] = 4.0 + 4.0*math.sin(self.Multiplier[c+i]*self.MainPhase)
        # Then call all pixels one by one to calc themselves,
        #   while append their return values to the display vector
        for pobj in PixList : V.append(pobj.calc())
        # Now step the phase
        self.MainPhase += StepAngle


# This stores the pixel data
class Pixel :

    def __init__(self,XC:int,YC:int) :
        self.R :int =0
        self.G :int =0
        self.B :int =0
        self.X :int =XC
        self.Y :int =YC

#    def display(self) :
#        s.setPixel(X,Y,R,G,B)

    def calc(self) -> list :
        global Fade
        distR :float = math.sqrt( (self.X-p.Coord["RX"])**2 + (self.Y-p.Coord["RY"])**2)
        distG :float = math.sqrt( (self.X-p.Coord["GX"])**2 + (self.Y-p.Coord["GY"])**2)
        distB :float = math.sqrt( (self.X-p.Coord["BX"])**2 + (self.Y-p.Coord["BY"])**2)
        self.R = int( 255.0 * Fade**distR )
        self.G = int( 255.0 * Fade**distG )
        self.B = int( 255.0 * Fade**distB )
        return list((self.R,self.G,self.B))


# This handles the stick events
def handle_stick(event) -> None :
    global Fade, SleepTime, StayInMainLoop
    if event.action != "pressed" : return
    if event.direction == "up" :
        Fade = Fade * 1.01
    elif event.direction == "down" :
        Fade = Fade * 0.99
    elif event.direction == "left" :
        SleepTime = SleepTime * 1.1
    elif event.direction == "right" :
        SleepTime = SleepTime * 0.9
    elif event.direction == "middle" :
        StayInMainLoop = False



# Kick off the main program
s=SenseHat()
s.clear()
s.stick.direction_any = handle_stick

# References to pixel objects
PixList :list =list(())
# Stores the vector to display
V :list =list(())

# Set up the 64 object references
for j in range(8) :
    for i in range(8) :
        PixList.append(Pixel(i,j))

# Set up the program variables
p = Program()


# Main loop
while StayInMainLoop:

    p.calc()
    s.set_pixels(V)
    sleep(SleepTime)

s.clear()
