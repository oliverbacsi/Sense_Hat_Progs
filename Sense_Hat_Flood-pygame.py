#!/usr/bin/env python3
#################################################
# The classic Color Flood game for Sense Hat
#

import random,time
import pygame
import pygame.locals as pgl
#from _sense_hat_ANSI import SenseHat
from sense_hat import SenseHat

#################### INIT PART ####################

COLOR :dict = {'_':[0,0,0], 'R':[180,0,0], 'O':[170,100,0], 'Y':[160,160,0], 'G':[0,180,0], 'C':[0,160,160], 'B':[0,0,180], 'M':[160,0,160], 'X':[255,255,255]}
# Index is first letter of the color, except '_' is background and 'X' is cursor or marker


#################### CLASS PART ####################

class Cell :
    """Object class for one cell of the 8x8 field"""

    def __init__(self, myX :int, myY :int) :
        global COLOR
        """Initialize the cell with its on-screen position"""
        self.X :int = myX
        self.Y :int = myY
        self.C :str = '_'
        while self.C not in ['R','O','Y','G','C','B','M'] : self.C = random.choice(list(COLOR.keys()))
        # links to the neighbouring cells
        self.Neigh :dict = dict(())
        for i in ['N','E','W','S'] : self.Neigh[i] = None
        self.draw()

    def draw(self) -> None :
        """Draw myself on the 8x8 screen"""
        global COLOR
        s.set_pixel(self.X, self.Y, COLOR[self.C])

    def changeColor(self, newCol :str, animate :bool =False) -> None :
        """Change the color of the cell after its creation.
        Parameters :
        :param newCol : The letter of the new color (as str)
        :param animate : Whether the change should be highlighted on the screen (as bool, default : False)
        :returns : None
        """
        global COLOR
        if newCol not in COLOR.keys() : return
        if animate :
            self.C = 'X'
            self.draw()
            time.sleep(0.05)
        self.C = newCol
        self.draw()

    def linkNeighbour(self, direction :str, cellObject) -> None :
        """Link the neighbouring cell.
        Parameters :
        :param direction : which direction is the neighbour ('N','E','W','S') as str
        :param cellObject : the object handle of the neighbouring cell
        :returns : None
        """
        if direction in ['N','E','W','S'] : self.Neigh[direction] = cellObject

    def getColor(self) -> str :
        """Return the actual color"""
        return self.C

    def flood(self, newColor :str) -> None:
        """Recursively flood with a new specified color
        Parameters :
        :param newColor : the letter index of the new color as str
        :returns : None
        """
        if newColor not in COLOR.keys() : return
        if newColor == self.C : return
        # Need to store what was my original color:
        prevColor = self.C
        self.changeColor(newColor,True)
        for direction in ['N','E','S','W'] :
            if self.Neigh[direction] :
                # If my direct neighbour has the same color as I did previously:
                if self.Neigh[direction].getColor() == prevColor :
                    self.Neigh[direction].flood(newColor)


class Game :
    """The object to store the game parameters"""

    def __init__(self) :
        """Initialize the Game"""
        self.Steps :int = 0
        self.Board :list = list(())
        # Cursor position, enabled, blink status
        self.CurX  :int = 0
        self.CurY  :int = 0
        self.CurE  :bool = True
        self.CurS  :bool = True
        self.GameOver :bool = False
        # Generate the 8x8 cells with random color
        for j in range(8) :
            for i in range(8) :
                self.Board.append(Cell(i,j))
        # Now link the neighbours where applicable
        for j in range(8) :
            for i in range(8) :
                if j   : self.Board[8*j+i].linkNeighbour('N',self.Board[8*j+i-8])
                if i   : self.Board[8*j+i].linkNeighbour('W',self.Board[8*j+i-1])
                if i<7 : self.Board[8*j+i].linkNeighbour('E',self.Board[8*j+i+1])
                if j<7 : self.Board[8*j+i].linkNeighbour('S',self.Board[8*j+i+8])
        # Now add some routines here to create smaller areas of similar colors
        # instead of only having isolated cells each with different color
        # The higher range is given to 'k', the more areas will exist
        for k in range(20) :
            # pick a random coordinate and direction
            c = random.randint(0,63)
            d = random.choice(['N','E','W','S'])
            # if neighbour exists, copy its color
            n = self.Board[c].Neigh[d]
            if n : self.Board[c].changeColor(n.getColor(),False)

    def colorClicked(self) -> None :
        """Handle the event when a cell is clicked with the stick"""
        # Switch off the cursor blinking first and restore original cell color
        self.CurE = False
        self.CurS = False
        CurObj = self.Board[8*self.CurY+self.CurX]
        CurObj.draw()
        CurCol = CurObj.getColor()
        # Check if the same color was clicked as we already have flooded
        if CurCol == self.Board[0].getColor() : return
        # Flood starting with the top-left cell
        # It is enough to call the method for the first cell
        # as the recursive algorhythm will call all direct neighbours
        # until the whole area is filled
        # Recursion will not be infinite as there will be no call-back from neighbour to self,
        # since we change ourself's color first before calling the neighbour,
        # causing that the neighbour does not see itself's own color on us any more, so not calling us back.
        self.Board[0].flood(CurCol)
        self.Steps += 1
        # Check if the board is complete. One single different color means: not complete.
        BoardComplete :bool = True
        for c in range(64) :
            if self.Board[c].getColor() != CurCol :
                BoardComplete = False
                break
        # If the board is complete, game over, otherwise enable the cursor blinking
        if BoardComplete :
            self.GameOver = True
        else :
            self.CurE = True

    def curChange(self) -> None :
        """Change the status of the cursor on the screen"""
        global COLOR
        if not self.CurE : return
        self.CurS = not self.CurS
        if self.CurS :
            s.set_pixel(self.CurX,self.CurY,COLOR['X'])
        else :
            self.Board[8*self.CurY+self.CurX].draw()


#################### PROC PART ####################

def clamp(Value :int) -> int :
    """Limit the incoming value to 0..7"""
    return max(min(Value,7),0)

def handle_event(event) -> None :
    """Handle pygame key hit events"""
    if event.type != pgl.KEYDOWN : return
    if event.key in [pgl.K_SPACE, pgl.K_RETURN] :
        g.colorClicked()
    else :
        ek = str(event.key)
        if ek not in ["273", "274", "275", "276"] : return
        g.CurE = False
        g.Board[8*g.CurY+g.CurX].draw()
        dt = {"273":(0,-1) , "274":(0,1) , "276":(-1,0) , "275":(1,0)}[ek]
        g.CurX = clamp(g.CurX+dt[0]) ; g.CurY = clamp(g.CurY+dt[1])
        g.CurE = True


#################### MAIN PART ####################

s = SenseHat()
s.clear()
g = Game()
pygame.init()
pygame.display.set_mode((400, 400))

while not g.GameOver :
    for event in pygame.event.get(): handle_event(event)
    g.curChange()
    time.sleep(0.5)

time.sleep(1)
for i in range(20) :
    (r1,g1,b1) = s.get_pixel(0,0)
    (r1,g1,b1) = (int(0.95*r1), int(0.95*g1), int(0.95*b1))
    s.clear([r1,g1,b1])
    time.sleep(0.1)
s.clear()
s.show_message(f"{g.Steps} steps used.")
pygame.quit()