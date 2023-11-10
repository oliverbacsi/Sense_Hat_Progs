#!/usr/bin/env python3
##################################################
# Aquarium

from sense_hat import SenseHat
#from _sense_hat_ANSI import SenseHat

from random import randint as r
from time import sleep
import math

#Initialize the screen and get the pixel vector
s=SenseHat()
s.clear([0,0,48])
V = s.get_pixels()

#Ticker is the "heartbeat" of the animation:
#Each screen element moves after certain ticks.
Ticker :int =0

#How many fish and bubbles simultaneously on the screen?
NumFish :int =6
NumBubble :int =3



# Define a class for the Fish objects:
class Fish :

    def __init__(self) :
        """Store the variables and methods of a Fish"""
        # Color triplet on the screen
        self.Color :list = list((r(128,255), r(128,255), r(128,255)))
        # Size is 1x1 or 2x1
        self.Size  :int  = r(1,2)
        # Slowness means how many ticks to wait until move. Large fish swims slower.
        self.Slow  :int  = r(2,5) + (self.Size-1)*3
        # Position and swim direction on the screen
        self.Dir   :int  = 1 if r(0,1) else -1
        self.XPos  :int  = -1 if self.Dir > 0 else 8
        self.YPos  :int  = r(0,5)

    def handleTick(self) -> None :
        """Handle the event if received a Tick"""
        global Ticker

        #if it's not our time to step, then return
        if Ticker % self.Slow : return

        #Step in the proper direction.
        #Possible feature : create "floating" effect by stepping one row up&down
        #Possible feature : as a fish "wobbles" it changes its shinyness, so could flicker the color a little bit
        self.XPos += self.Dir

    def draw(self) -> None :
        """Draw the fish on the pixel Vector"""
        global V

        # For safety reasons check if we are still on the screen
        if self.XPos in range(8) : V[self.YPos*8+self.XPos] = self.Color

        # For small fish that's it. For large fish let's check if we need to draw the tail
        if self.Size < 2 : return
        TailPos :int = self.XPos - self.Dir
        if TailPos in range(8) : V[self.YPos*8+TailPos] = self.Color

    def hasLeft(self) -> bool :
        """Check if fish has already left the screen"""
        # We could make a difference now based on fish size to check the tail as well,
        # but it's not worth it, let's simply check if the "head" has left the proximity of the screen.
        return self.XPos not in range(-1,9)



# Define a class for the SeaWeed objects:
class SeaWeed :

    def __init__(self) :
        """Store the parameters and methods of the SeaWeeds"""
        # Because of the sinusoid movement there will be 0.5 pixel added to the X position,
        # so the centerline of the weed is always between 2 pixels, therefore
        # the random range is only 0..6  meaning that the center line will be on 0.5 ... 6.5
        self.XPos :float = 0.5 + r(0,6)
        # The waving phase of the Weed: Current and Step
        self.CurrPhase :float = 0.1 * r(0,10)
        self.PhaseStep :float = 0.5 + 0.1*r(0,10)
        # How many ticks to wait between updates
        self.Slow :int = r(5,10)
        # Randomize the color a little
        self.Color :list = list((0,r(48,75),0))
        # How tall we grow
        self.Height :int = r(4,6)

    def handleTick(self) -> None :
        """Handle the event if received a Tick"""
        global Ticker

        #if it's not our time to step, then return
        if Ticker % self.Slow : return

        #Increase the waving phase, truncate the float after 10 full cycles
        self.CurrPhase = self.CurrPhase + self.PhaseStep
        if self.CurrPhase > 628.31853 : self.CurrPhase = self.CurrPhase - 628.31853

    def draw(self) -> None :
        """Draw the SeaWeed on the pixel Vector"""
        global V

        RealX :int
        for j in range(self.Height) :
            RealX = int( self.XPos + 0.6*math.sin(self.CurrPhase + 1.5*j) )
            V[(6-j)*8+RealX] = self.Color



# Define a class for the Bubble objects:
class Bubble :

    def __init__(self) :
        """Store the parameters and methods of the Bubbles"""
        # Where does the bubble raise
        self.XPos :int = r(0,7)
        # Make sure the bubbles are spread and also don't come immediately
        self.YPos :int = r(8,16)
        # Randomize the color a little
        self.Color :list = list((0,0,r(120,180)))

    def handleTick(self) -> None :
        """Handle the event if received a Tick"""
        global Ticker
        #Let the bubbles raise quickly
        self.YPos -= 1

    def draw(self) -> None :
        """Draw the Bubble on the pixel Vector"""
        global V
        if self.YPos in range(8) : V[self.YPos*8+self.XPos] = self.Color

    def hasLeft(self) -> bool :
        """Check if bubble has already left the surface"""
        return self.YPos < 0




########## MAIN PROG ##########

# Let's create all the stuff
# One weed in front of the fish, one behind
weedbg = SeaWeed()
weedfg = SeaWeed()

# Pick a quantity for the fish simultaneously on the screen:
fish :list =list(())
for i in range(NumFish) : fish.append(Fish())

# Pick a quantity for the bubbles simultaneously on the screen:
bubble :list =list(())
for i in range(NumBubble) : bubble.append(Bubble())


# MAIN LOOP
while True:

    # Water (a bit flickering)
    for i in range(48) : V[i] = list((0,0,r(48,72)))

    # Sand (somewhat flickering as well)
    for i in range(48,64) :
        R = r(48,72)
        V[i] = list((R,R,0))

    # Change the sequence of the below drawing routines to move the items forward/backward

    # Weed in the background should come first:
    weedbg.handleTick()
    weedbg.draw()

    # Then the fish:
    for i in range(NumFish) :
        fish[i].handleTick()
        fish[i].draw()
        # If the fish swam out of the screen, drop the object and generate a new
        if fish[i].hasLeft() : fish[i] = Fish()

    # Next is Weed in the foreground:
    weedfg.handleTick()
    weedfg.draw()

    # Finally add some bubbles:
    for i in range(NumBubble) :
        bubble[i].handleTick()
        bubble[i].draw()
        # If a bubble has reached the surface, drop the object and generate a new
        if bubble[i].hasLeft() : bubble[i] = Bubble()

    # Increase the ticker, draw the pixel vector on the screen, wait
    Ticker += 1
    s.set_pixels(V)
    sleep(0.15)

