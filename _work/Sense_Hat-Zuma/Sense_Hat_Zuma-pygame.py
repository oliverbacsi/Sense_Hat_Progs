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

COLOROF :list = [(48,48,48), (255,0,0), (255,255,0), (0,255,0), (80,80,255), (255,0,255), (255,160,0), (0,200,255), (220,220,220)]


#################### CLASS PART ####################

class Game :

    def __init__(self) :
        global PATHPOSITIONS
        # Game Level
        self.Level :int =0
        # Number of different colors for balls
        self.NumColor :int =2
        # Number of "snake length", total balls initiated
        self.NumBalls :int =45
        # Number of Balls Left on the level
        self.NumBallsLeft :int =45
        # Player lives
        self.Lives :int =3
        # Path Length
        self.PathLen :int = len(PATHPOSITIONS)
        # Ball data on the Game Path
        self.Cells :str =""
        # Inertia signalizes which direction the balls are moving
        # Default value should be 1, meaning balls are being pushed from the entry point
        # 0 means they are stopped
        # Negative value means that some vacancy is pulled together, moving the right group backwards
        # -3 is a good idea as this means that the whole queue is stopped for 3 turns before it restarts
        self.Inertia :int =1
        # This ensures that even of ticking with 200ms, the balls only step at every 1s
        self.Ticker :int =0
        # List of indexes of first balls that need to be attracted left
        self.AttractionIndices :list = list(())


    def newLevel(self) -> None :
        """Initialize a new level with more ball colors and longer train"""
        self.Level += 1
        self.NumColor = min(8,self.NumColor+1)
        self.NumBalls += 5
        self.NumBallsLeft = self.NumBalls
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
        # Set up one more cell after the last one in the path
        # That can be used to check if the first ball has hit the wall
        self.Cells = "0"*(self.PathLen+1)
        self.AttractionIndices = []
        self.Inertia = 1
        self.drawPath()


    def drawPath(self) -> None :
        """Draw the Game Path on the screen."""
        global PATHPOSITIONS,COLOROF
        for i in range(self.PathLen) :
            p = PATHPOSITIONS[i]
            s.set_pixel(p[0],p[1],COLOROF[self.Cells[i]])


    def isGameOver(self) -> bool :
        """Checks if the first ball has moved too far and hit the shooting position.
        :returns: True if game was lost."""
        return self.Cells[-1] != "0"

    def isGameWon(self) -> bool :
        """Checks if player has won the level.
        Meaning: Whole play field is clear and there are no more Balls to insert.
        :returns: True if game is won."""
        if self.NumBallsLeft : return False
        return self.Cells == "0"*(self.PathLen+1)

    def checkAttractions(self) -> None :
        """Collect all locations where similar balls are on both edges of a hole,
        and store the right side ball's index in the AttractionIndices,
        as well as the end indices of the trains,
        as these balls need to be pulled backwards."""
        self.AttractionIndices = []
        lastValid :str ='e'
        prevZero :bool =False
        st :int =-1
        for i in range(self.PathLen) :
            if self.Cells[i] == '0' :
                prevZero = True
            else :
                if prevZero :
                    if lastValid == self.Cells[i] :
                        st=i
                        while self.Cells[i] != '0' : i+=1
                        self.AttractionIndices.append(list((st,i-1)))
                        lastValid = self.Cells[i-1]
                        prevZero = True
                prevZero = False
                lastValid = self.Cells[i]

    def pullBack(self, Start :int, End :int) -> None :
        """Execute the ball train pull back at certain index.
        Parameters:
        :param Start: leftmost ball position in the train
        :param End: rightmost ball position in the train
        :returns : None"""
        if Start > End : return
        if End >= self.PathLen : return
        if self.Cells[Start-1] != "0" : return
        c1 :str = self.Cells[0:Start-1]+self.Cells[Start:End+1]+"0"+self.Cells[End+1:]
        self.Cells = c1[0:self.PathLen+1]
        self.Inertia = -3

    def pushTrain(self) -> None :
        """Push the train one forward at its beginning."""
        if self.Inertia < 1 : return
        # Search for the beginning of the first train (the first non-zero cell)
        # This might be immediately at the beginning (normally)
        # or somewhere mid-field (during the end game)
        Start :int =0
        while (Start < self.PathLen) and (self.Cells[Start] == "0") : Start += 1
        End :int =Start
        while (End < self.PathLen) and (self.Cells[End] != "0") : End += 1
        if Start :
            c1 :str = "0"*(Start+1) + self.Cells[Start:End] + self.Cells[End+1:]
        else :
            c1 :str = self.getRandomBall() + self.Cells[Start:End] + self.Cells[End+1:]
        self.Cells = c1[0:self.PathLen+1]

    def getRandomBall(self) -> str :
        """Random generate a new ball color to be pushed at the front."""
        # If the necessary number of balls have been generated, then return empty
        if not self.NumBallsLeft : return "0"
        ret :int = random.randint(1,self.NumColor)
        # Don't generate a sequence of 3 equal balls
        while (str(ret) == self.Cells[0]) and (str(ret) == self.Cells[1]) : ret = random.randint(1,self.NumColor)
        self.NumBallsLeft -= 1
        return str(ret)

    def eliminateSimilars(self) -> None :
        """Search for consecutive 3 or more Balls and eliminate them"""
        seqStart :int =-1  # Since which idx do we have consecutive balls
        seqVal   :str ='e' # of what value
        seqLen   :int =-1  # Length of consecutive balls
        for i in range(self.PathLen) :
            if self.Cells[i] == seqVal :
                seqLen += 1
            else :
                if seqLen > 2 :
                    for j in range(seqStart,seqStart+seqLen) :
                        self.Cells[j] = '0'
                    # Stop for a moment if there was something to eliminate
                    self.Inertia = -1
                seqVal = self.Cells[i]
                seqLen = 1
                seqStart = i

    def tryInsertBallAt(self, Pos :int, Ball :str) -> bool :
        """Try to insert a certain color of Ball into a certain Position.
        Parameters:
        :param Pos: Index of Cell where the Ball would like to go to.
        :param Ball: Ball color as single digit string
        :returns: True if insertion was successful."""
        # Possibilities:
        # The cell is occupied:
        #  - Move all balls to the right, starting from the targeted cell,
        #    ending at the first '0' (or at the end of the train)
        # The cell is free ('0'):
        #  - Is at least one of the neighbours non-zero? (to stick the ball to)
        #    - Then the respective cell should get the Ball and that's it
        #  - Both neighbours are zero, so totally empty area:
        #    - Ball flies through and False is returned
        if self.Cells[Pos] == "0" :
            if self.Cells[Pos-1:Pos+1] == "000" : return False
            self.Cells[Pos] = Ball
            return True
        else :
            End :int =Pos
            while (End < self.PathLen) and (self.Cells[End] != "0") : End += 1
            c1 :str = self.Cells[0:Pos] + Ball + self.Cells[Pos:End] + self.Cells[End+1:]
            self.Cells = c1[0:self.PathLen+1]







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
