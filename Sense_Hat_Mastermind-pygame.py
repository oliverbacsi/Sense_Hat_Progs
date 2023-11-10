#!/usr/bin/env python3
###################################################
# Mastermind Game for SenseHat
#

#################### INIT PART ####################

import random, time, math
import pygame
import pygame.locals as pgl
#from _sense_hat_ANSI import SenseHat
from sense_hat import SenseHat

# Peg colors the game is allowed to use (6 colors by default) are under '_'
COLOR :dict = {'R':(240,0,00), 'Y':(200,200,0), 'G':(00,240,0),  'C':(0,200,200), 'B':(0,0,240), 'M':(200,0,200),
               'x':(0,0,0)   , 'w':(60,60,120), 'b':(60,180,60), 'e':(0,160,210),
               '_':('R','Y','G','C','B','M')}


#################### CLASS PART ####################

class Game :
    """Store the general methods and variables"""

    def __init__(self) :
        # Stores the list of player guesses
        self.GuessList :list =list(())
        # Stores the list of results
        self.ResultList :list =list(())
        # Which is the first Guess to show in the top row
        self.ViewStart :int =0
        # View previous steps or enter a new guess  (default is enter the first guess)
        self.EnterMode :bool =True
        # Cursor X position when in enter mode
        self.CurX :int =0
        # Computer's guess
        self.myGuess :list =list(())
        # Guess being made by player
        self.GuessInProgress :list =list(())
        # Stay in the game main loop until the game is over
        self.StayInMainLoop :bool =True


    def newGame(self) -> None :
        """Restarts an empty game"""
        global COLOR
        self.GuessList =list(())
        self.ResultList =list(())
        self.ViewStart =0
        self.EnterMode =True
        self.CurX =0
        self.myGuess =list(())
        self.GuessInProgress = ['x','x','x','x']
        # Computer make a guess
        for i in range(4): self.myGuess.append(random.choice(COLOR['_']))
        self.redrawScreen()

    def redrawScreen(self) -> None :
        """Redraw the whole screen based on the guesses, results and where the screen view starts"""
        global COLOR
        s.clear()
        # Determine the range of guesses to display on the screen
        Fr :int =self.ViewStart
        To :int =min(self.ViewStart+7,len(self.GuessList))
        # j is the Y coordinate on the screen
        j :int =0
        # k is the "Y coordinate" of the guess list
        for k in range(Fr,To) :
            # Draw the player's guess in the left 4 columns
            for i in range(4) :
                s.set_pixel(i,j,COLOR[self.GuessList[k][i]])
            # Draw the response lights aligned right. l is the X coordinate on the screen
            l = 7
            for c in self.ResultList[k] :
                s.set_pixel(l,j,COLOR[c])
                l-=1
            j+=1
        # Finally put the in-progress guess at the bottom
        self.redrawEditedRow()

    def redrawEditedRow(self) -> None :
        """Redraw the bottom row of the screen"""
        global COLOR
        for i in range(4) :
            s.set_pixel(i,7,COLOR[self.GuessInProgress[i]])
        for i in range(4,8) :
            s.set_pixel(i,7,[0,0,0])
        # If player is entering a guess, display the "Enter Button" as well:
        if self.EnterMode :
            s.set_pixel(7,7,COLOR['e'])


    def gameOver(self) -> None :
        self.StayInMainLoop = False

    def recalcResults(self, itemNum :int =-1) -> None :
        """Calculate the results of a guess or all guesses.
        Params:
        :param itemNum : Which item in the list to calculate, as int
        (defaults to -1, which means all items.)
        :returns : None"""

        # If there is no guess made, just return silently
        if not len(self.GuessList) : return

        # If negative index is requested, process the whole guess list
        if itemNum < 0 :
            Fr :int =0
            To :int =len(self.GuessList)
        else :
            # Requested item index exceeds the list
            if itemNum >= len(self.GuessList) : return
            # From-To range will be a single item
            Fr :int =itemNum
            To :int =itemNum+1

        # Now let's go trhough the requested range
        for i in range(Fr,To) :
            # Erase whatever is in the results
            self.ResultList[i] = []
            # Track which of the 4 pegs have been reported already as full match
            Reported = [False, False, False, False]
            for j in range(4) :
                if self.myGuess[j] == self.GuessList[i][j] :
                    # We have a full match, give a black flag as result and mark the color as reported
                    Reported[j] = True
                    self.ResultList[i].append("b")
            # Collect peg colors which didn't have a full match therefore not yet reported,
            # so they are the ones available for the check whether at least the color matches.
            RemainingColors = list(())
            for j in range(4) :
                if not Reported[j] :
                    RemainingColors.append(self.myGuess[j])
            # For all pegs not yet reported to a color check only without location
            for j in range(4) :
                if not Reported[j] :
                    if self.GuessList[i][j] in RemainingColors :
                        self.ResultList[i].append("w")


    def handleEvent(self, event) -> None :
        """Handle pygame key events, depending which mode we are in."""
        global COLOR
        if event.type != pgl.KEYDOWN : return

        # If player is setting up a guess
        if self.EnterMode :
            if event.key in [pgl.K_SPACE, pgl.K_RETURN] :
                if self.CurX == 7 :
                    # The player clicked on the "Enter" button, let's check if it is a valid guess
                    _validGuess = True
                    for w in range(4) :
                        if self.GuessInProgress[w] not in COLOR['_'] : _validGuess = False
                    if _validGuess :
                        self.EnterMode = False
                        self.GuessList.append(self.GuessInProgress)
                        self.ResultList.append([])
                        self.GuessInProgress = ['x', 'x', 'x', 'x']
                        self.ViewStart = max(0,len(self.GuessList)-7)
                        self.redrawScreen()
                        self.recalcResults(len(self.GuessList)-1)
                        q3 = 7
                        for r3 in self.ResultList[-1] :
                            time.sleep(1)
                            s.set_pixel(q3,6,COLOR[r3])
                            q3 -=1
                        time.sleep(1)
                        flash("bot",[60,170,240])
                        self.CurX =0
                        self.redrawScreen()
                        # Check if game is over
                        if self.ResultList[-1] == ['b', 'b', 'b', 'b']: self.gameOver()
                    else :
                        flash("bot",[255,0,60])
                else :
                    # Otherwise just step out of the "Editor Mode"
                    self.EnterMode = False
            else :
                # Handle stick movements in Editor Mode
                if event.key == 276 :
                    self.CurX = (self.CurX-1)%8
                    self.redrawEditedRow()
                elif event.key == 275 :
                    self.CurX = (self.CurX+1)%8
                    self.redrawEditedRow()
                elif event.key == 273 :
                    if self.CurX in range(4) :
                        c = self.GuessInProgress[self.CurX]
                        if c == 'x' :
                            self.GuessInProgress[self.CurX] = 'R'
                        else :
                            self.GuessInProgress[self.CurX] = COLOR['_'][(COLOR['_'].index(c)+1) % len(COLOR['_'])]
                        self.redrawEditedRow()
                elif event.key == 274 :
                    if self.CurX in range(4) :
                        c = self.GuessInProgress[self.CurX]
                        if c == 'x' :
                            self.GuessInProgress[self.CurX] = 'M'
                        else :
                            self.GuessInProgress[self.CurX] = COLOR['_'][(COLOR['_'].index(c)-1) % len(COLOR['_'])]
                        self.redrawEditedRow()

        # If player is just browsing between previous guesses
        else :
            if event.key in [pgl.K_SPACE, pgl.K_RETURN] :
                self.EnterMode = True
            elif event.key in range(273,277) :
                dt = {"273":-1, "274":1, "275":0, "276":0}[str(event.key)]
                self.ViewStart += dt
                # Flash if screen can not be scrolled any more
                if self.ViewStart < 0 :
                    self.ViewStart = 0
                    flash("top",[255,60,60])
                elif self.ViewStart > len(self.GuessList)-7 :
                    self.ViewStart = max(0,len(self.GuessList)-7)
                    flash("bot",[255,60,60])
            self.redrawScreen()



#################### PROC PART ####################


def flash(what :str ="scr", colorList :list =[255,255,255]) -> None :
    """Do a warning flash on the screen.
    Params:
    :param what : "top" row, "bot" row, or "scr" for whole screen (default)
    :param colorList : The [R,G,B] color list of the flash. (default: bright white)
    :returns : None"""
    # Save the image from the screen first
    save :list = s.get_pixels()
    if what == "scr" :
        s.set_pixels([colorList] *64)
    elif what == "top" :
        for i in range(8) : s.set_pixel(i,0,colorList)
    else :
        for i in range(8) : s.set_pixel(i,7,colorList)
    time.sleep(0.4)
    s.set_pixels(save)



#################### MAIN PART ####################

s = SenseHat()
s.clear()
pygame.init()
pygame.display.set_mode((400, 400))
g = Game()
g.newGame()


# Staying within the main loop is basically to blink the cursor as everything else is driven by stick events
# and handled by embedded methods of the Game object g.
while g.StayInMainLoop :
    for event in pygame.event.get(): g.handleEvent(event)
    if g.EnterMode :
        if g.CurX < 4 :
            if g.GuessInProgress[g.CurX] == 'x' :
                _col = [240,240,240]
            else :
                _col = [0,0,0]
        elif g.CurX < 7 :
            _col = [240,240,240]
        else :
            _col = [0,0,0]
        s.set_pixel(g.CurX,7,_col)
        time.sleep(0.3)
        g.redrawEditedRow()
    time.sleep(0.8)


# Flash the screen, fade away, then show the results
for q in range(3) :
    flash("scr",[60,240,180])
    time.sleep(0.7)
time.sleep(2)

V = s.get_pixels()
for q1 in range(40):
    for q2 in range(64):
        (rx, gx, bx) = V[q2]
        rx = math.floor(rx * 0.95) ; gx = math.floor(gx * 0.95) ; bx = math.floor(bx * 0.95)
        V[q2] = [rx, gx, bx]
    s.set_pixels(V)
    time.sleep(0.1)
s.clear()
s.show_message(f"{len(g.GuessList)} steps used.", text_colour=[60,240,180])
pygame.quit()
