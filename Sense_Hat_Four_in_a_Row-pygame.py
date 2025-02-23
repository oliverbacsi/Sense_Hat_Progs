#!/usr/bin/env python3
#################################################
# Four-in-a-row game for SenseHat
#

import random,time
import pygame
import pygame.locals as pgl
try :
    from sense_hat import SenseHat
except :
    try :
        from sense_emu import SenseHat
    except :
        from _sense_hat_ANSI import SenseHat


#################### INIT PART ####################

# The 10 different colors (apart from white) to display
COLOROF :list = [(0,0,0), (255,0,0), (0,255,0), (80,80,255), (255,255,0), (0,160,255), (255,0,160), (255,160,0), (150,150,150), (160,0,255), (0,255,160)]


#################### CLASS PART ####################

class Game :

    def __init__(self) :
        # Number of possible different colors for balls
        # Min = 3 ; Max = 10
        self.NumColor :int =6
        # Number of matching balls in a row to consider it completed
        # Min = 3 ; Max = 6
        self.FullRow :int =4
        # Number of balls injected in case no row was removed
        # Min = 1 ; Max = 5
        self.InjectBalls :int =2
        # The Game Field
        self.Board :list = [0] *64
        # Points earned
        self.Points :int =0
        # Is the game over?
        self.GameOver :bool =False
        # Cursor coordinates, Enablement and On Status
        self.cX :int =-1
        self.cY :int =-1
        self.cE :bool =True
        self.cS :bool =True


    def redrawScreen(self) -> None :
        """Redraw the Sense Hat LED screen based on the Game field"""
        global COLOROF
        Vector :list = list(())
        for i in self.Board : Vector.append(COLOROF[i])
        s.set_pixels(Vector)

    def checkGameOver(self) -> None :
        """Check if game is over and set attribute accordingly"""
        Num :int =0
        for i in self.Board :
            if i == 0 : Num += 1
        if Num < self.InjectBalls : self.GameOver =True



#################### PROC PART ####################


def fadeAway() -> None :
    """Fade the current screen away."""
    V = s.get_pixels()
    for q1 in range(40):
        for q2 in range(64):
            (rx, gx, bx) = V[q2]
            rx = math.floor(rx * 0.95) ; gx = math.floor(gx * 0.95) ; bx = math.floor(bx * 0.95)
            V[q2] = [rx, gx, bx]
        s.set_pixels(V)
        time.sleep(0.1)
    s.clear()


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
pygame.init()
pygame.display.set_mode((400, 400))

g = Game()
g.redrawScreen()

while not g.GameOver :
    for event in pygame.event.get(): handleEvent(event)
    if g.cE :
        g.cS = not g.cS
        g.redrawScreen()
        if g.cS : s.set_pixel(g.cX, g.cY, (255,255,255))
    time.sleep(0.5)

time.sleep(3)
fadeAway()
s.show_message(f"GAME OVER. Points: {g.Points}")

s.clear()
pygame.quit()
