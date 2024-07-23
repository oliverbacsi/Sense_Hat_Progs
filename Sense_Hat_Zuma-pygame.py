#!/usr/bin/env python3
#################################################
# The classic Color Flood game for Sense Hat
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

PATHPOSITIONS :list =list(())
for i in range(0,8) : PATHPOSITIONS.append([i,0])
for i in range(1,8) : PATHPOSITIONS.append([7,i])
for i in range(1,8) : PATHPOSITIONS.append([7-i,7])
for i in range(1,6) : PATHPOSITIONS.append([0,7-i])
for i in range(1,6) : PATHPOSITIONS.append([i,2])
for i in range(3,6) : PATHPOSITIONS.append([5,i])
for i in range(3,6) : PATHPOSITIONS.append([7-i,5])
PATHPOSITIONS.append([2,4])

LETTERREL :dict =dict(())
LETTERREL["0"] = [[0,0],[1,0],[2,0],[2,1],[2,2],[2,3],[2,4],[1,4],[0,4],[0,3],[0,2],[0,1]]
LETTERREL["1"] = [[0,1],[1,0],[1,1],[1,2],[1,3],[1,4],[0,4],[2,4]]
LETTERREL["2"] = [[0,0],[1,0],[2,0],[2,1],[2,2],[1,2],[0,2],[0,3],[0,4],[1,4],[2,4]]
LETTERREL["3"] = [[0,0],[1,0],[2,0],[2,1],[2,2],[1,2],[0,2],[2,3],[0,4],[1,4],[2,4]]
LETTERREL["4"] = [[2,0],[2,1],[2,2],[2,3],[2,4],[1,2],[0,2],[0,1],[0,0]]
LETTERREL["5"] = [[2,0],[1,0],[0,0],[0,1],[0,2],[1,2],[2,2],[2,3],[2,4],[1,4],[0,4]]
LETTERREL["6"] = [[2,0],[1,0],[0,0],[0,1],[0,2],[1,2],[2,2],[2,3],[2,4],[1,4],[0,4],[0,3]]
LETTERREL["7"] = [[2,0],[2,1],[2,2],[2,3],[2,4],[1,0],[0,0]]
LETTERREL["8"] = [[0,0],[1,0],[2,0],[2,1],[2,2],[2,3],[2,4],[1,4],[0,4],[0,3],[0,2],[0,1],[1,2]]
LETTERREL["9"] = [[0,0],[1,0],[2,0],[2,1],[2,2],[2,3],[2,4],[1,4],[0,4],[0,2],[0,1],[1,2]]
LETTERREL["0h"] = [[0,0],[0,1],[0,2],[0,3],[0,4],[1,0],[1,1],[1,2],[1,3],[1,4]]
LETTERREL["1h"] = [[0,0],[0,1],[0,2],[0,3],[0,4]]
LETTERREL["5h"] = [[0,0],[0,1],[0,2],[0,4],[1,0],[1,2],[1,3],[1,4]]



#################### CLASS PART ####################

class Game :

    def __init__(self) :
        # Game Level
        self.Level :int =0
        # Number of different colors for balls
        self.NumColor :int =2
        # Number of "snake length", total balls initiated
        self.NumBalls :int =45
        # Player lives
        self.Lives :int =3


    def newLevel(self) -> None :
        self.Level += 1
        self.NumColor = min(8,self.NumColor+1)
        self.NumBalls += 5
        # Display lives number
        s.clear() ; time.sleep(0.5)
        for px in [[0,0],[0,1],[0,2],[1,2],[2,2],
                   [4,0],[5,0],[6,0],[5,1],[4,2],[5,2],[6,2]] :
            s.set_pixel(px[0],px[1],60,20,0)
        disp2(str(self.Lives).zfill(2),[150,50,0])
        time.sleep(4)
        # Display level number
        s.clear() ; time.sleep(0.5)
        for px in [[0,0],[0,1],[0,2],[1,2],[2,2],
                   [3,0],[4,1],[5,2],[6,1],[7,0]] :
            s.set_pixel(px[0],px[1],60,60,0)
        disp2(str(self.Level).zfill(2),[150,150,0])
        time.sleep(4)
        # Display color number
        s.clear() ; time.sleep(0.5)
        for px in [[2,0],[1,0],[0,0],[0,1],[0,2],[1,2],[2,2],
                   [4,0],[4,1],[4,2],[5,2],[6,2]] :
            s.set_pixel(px[0],px[1],0,60,0)
        disp2(str(self.NumColor).zfill(2),[0,150,0])
        time.sleep(4)
        # Display snake length
        s.clear() ; time.sleep(0.5)
        for px in [[0,0],[0,1],[0,2]] : s.set_pixel(px[0],px[1],0,60,60)
        for ix in range(0,8) :
            time.sleep(0.2)
            s.set_pixel(ix,1,0,60,60)
        time.sleep(0.2)
        for px in [[7,0],[7,2]] : s.set_pixel(px[0],px[1],0,60,60)
        time.sleep(0.5)
        if self.NumBalls > 199 :
            # Stupid failsafe solution:
            disp2(str(self.NumBalls)[-2:],[255,0,0])
        elif self.NumBalls > 99 :
            disp2_5(str(self.NumBalls),[0,150,150])
        else :
            disp2(str(self.NumBalls),[0,150,150])
        time.sleep(4)
        s.clear() ; time.sleep(0.5)




#################### PROC PART ####################


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


def disp2(txt,col) -> None :
    """Display 2 small 3x5 digits on the SenseHat aligned bottom-right"""
    global LETTERREL
    for Pos in LETTERREL[txt[0]] : s.set_pixel(1+Pos[0],3+Pos[1],col)
    for Pos in LETTERREL[txt[1]] : s.set_pixel(5+Pos[0],3+Pos[1],col)

def disp2_5(txt,col) -> None :
    """Display 2.5 small digits on the SenseHat aligned bottom"""
    global LETTERREL
    for Pos in LETTERREL[txt[0]+"h"] : s.set_pixel(0+Pos[0],3+Pos[1],col)
    for Pos in LETTERREL[txt[1]] : s.set_pixel(2+Pos[0],3+Pos[1],col)
    for Pos in LETTERREL[txt[2]+"h"] : s.set_pixel(6+Pos[0],3+Pos[1],col)



#################### MAIN PART ####################

s = SenseHat()
s.clear()
pygame.init()
pygame.display.set_mode((400, 400))

g = Game()
g.newLevel()

s.clear()
pygame.quit()
