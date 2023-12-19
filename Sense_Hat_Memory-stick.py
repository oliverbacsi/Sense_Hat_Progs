#!/usr/bin/env python3
#################################################
# The classic Memory game for Sense Hat
#

import random,time,math
try :
    from sense_hat import SenseHat
except :
    try :
        from sense_emu import SenseHat
    except :
        from _sense_hat_ANSI import SenseHat

#################### INIT PART ####################

COLOR :dict = {'_':[0,0,0], 'R':[180,0,0], 'O':[170,100,0], 'Y':[160,160,0], 'G':[0,180,0], 'C':[0,160,160], 'B':[0,0,180], 'M':[160,0,160], 'W':[150,150,150], '#':[255,255,255]}
# Index is first letter of the color, except '_' is background and '#' is cursor or marker
BCOLOR :dict = {'_':[0,0,0], 'R':[48,0,0], 'O':[64,48,0], 'Y':[48,64,0], 'G':[0,48,0], 'C':[0,48,48], 'B':[0,0,48], 'M':[48,0,48], 'W':[48,48,48], '#':[0,0,0]}


#################### CLASS PART ####################

class Cell :
    """Object class for one cell of the 4x4 field"""

    def __init__(self, myX :int, myY :int, myColor :str, myPattern :int) :
        global COLOR
        """Initialize the cell with its coordinates, color and pattern"""
        self.X :int = myX
        self.Y :int = myY
        # color is a single letter abbreviation from the COLOR[] dictionary keys
        self.C :str = myColor
        # Pattern is an integer between 1-15, (4 bits), highest bit (value 8) representing whether there is a pixel
        # in the top-left corner of the pattern, next bit (value 4) is for top-right corner's pixel,
        # third bit (value 2) is bottom-left, and lowest bit (value 1) is for the bottom-right corner pixel.
        self.P :int = myPattern
        # Below flag is to signalize if the matching square has been discovered already
        self.Discovered :bool =False
        # Below flag signalizes if the square has been called up for watching and finding its mate
        self.Addressed  :bool =False


    def draw(self, _Forced :bool =False) -> None :
        """Draw myself on the screen based on the status
        Parameters:
        :param _Forced : Draw anyway, ignoring all statuses (as bool, default =False)
        :returns : None"""
        global COLOR
        global BCOLOR
        cx, cy = 2*self.X, 2*self.Y
        # If we have to draw, then the "highlighted" pixel will be the self.Color, otherwise it will be also the background color.
        Pix = COLOR[self.C] if self.Discovered or self.Addressed or _Forced else COLOR['_']
        BPix = BCOLOR[self.C] if self.Discovered or self.Addressed or _Forced else BCOLOR['_']
        s.set_pixel(cx  ,cy  ,Pix if self.P&8 else BPix)
        s.set_pixel(cx+1,cy  ,Pix if self.P&4 else BPix)
        s.set_pixel(cx  ,cy+1,Pix if self.P&2 else BPix)
        s.set_pixel(cx+1,cy+1,Pix if self.P&1 else BPix)


    def getColor(self) -> str :
        """Return the actual color abbreviation as string"""
        return self.C

    def getPattern(self) -> int :
        """Return the actual pattern as int"""
        return self.P


    def address(self) -> None :
        """Call the cell to show temporary"""

        # If I am already discovered, then ignore and do not count as a step
        if self.Discovered : return
        # Every other activity counts as a step
        g.Steps += 1
        # If I am the one already addressed before, then switch off the addressing
        if self.Addressed :
            self.unaddress()
            g.LastAddressed = None
            return
        # If an other square has been already addressed before, then check if it has the same color than myself
        if g.LastAddressed :
            g.LastAddressed.unaddress()
            # If it is the same color, then discover the last addressed and myself as well
            if g.LastAddressed.getColor() == self.C :
                g.LastAddressed.discover()
                self.discover()
                g.LastAddressed = None
                g.checkGameOver()
                return
        # Otherwise just make myself as the addressed square
        self.Addressed = True
        g.LastAddressed = self
        g.redraw()

    def unaddress(self) -> None :
        """Remove the addressing of the cell"""
        self.Addressed = False

    def discover(self) -> None :
        """Declare the cell as discovered"""
        self.Discovered = True



class Game :
    """The object to store the game parameters"""

    def __init__(self) :
        """Initialize the Game"""
        global COLOR

        self.Steps :int = 0
        self.Board :list = [None]*16
        # Cursor position, enabled, blink status
        self.CurX  :int = 0
        self.CurY  :int = 0
        self.CurE  :bool = True
        self.CurS  :bool = True
        # The last cell called up
        self.LastAddressed = None
        # Is the game over yet?
        self.GameOver :bool = False
        # Generate the colors, patterns and spread accross the board
        AllCols :set = set((COLOR.keys()))
        AllCols.discard('_') ; AllCols.discard('#')
        AllPatterns :set = set(())
        while len(AllPatterns) < 8 : AllPatterns.add(random.randint(1,15))
        AllCoords :list = list((range(16)))
        for i in range(8) :
            pat = random.choice(list(AllPatterns))
            AllPatterns.remove(pat)
            col = AllCols.pop()
            for j in range(2) :
                coo = random.choice(AllCoords)
                AllCoords.pop(AllCoords.index(coo))
                self.Board[coo] = Cell(coo%4,coo//4,col,pat)

    def redraw(self) -> None :
        """Redraw the screen"""
        for cell in self.Board : cell.draw()

    def curChange(self) -> None :
        """Change the status of the cursor on the screen"""
        global COLOR
        if not self.CurE : return
        self.CurS = not self.CurS
        if self.CurS :
            for dx,dy in [[0,0], [0,1], [1,0], [1,1]] :
                s.set_pixel(self.CurX*2+dx,self.CurY*2+dy,COLOR['#'])
        else :
            self.Board[4*self.CurY+self.CurX].draw()

    def checkGameOver(self) -> None :
        """Check if the game is over yet"""
        for cell in self.Board :
            if not cell.Discovered : return
        self.GameOver = True

    def cellClicked(self) -> None :
        """Manage the event that player clicked on the field"""
        self.Board[4*self.CurY+self.CurX].address()


#################### PROC PART ####################

def clamp(Value :int) -> int :
    """Limit the incoming value to 0..3"""
    return max(min(Value,3),0)

def handle_event(event) -> None :
    """Handle the stick events"""
    if event.action != "pressed" : return
    if event.direction == "middle" :
        g.cellClicked()
    else :
        g.CurE = False
        g.Board[4*g.CurY+g.CurX].draw()
        dt = {"up":(0,-1) , "down":(0,1) , "left":(-1,0) , "right":(1,0)}[event.direction]
        g.CurX = clamp(g.CurX+dt[0]) ; g.CurY = clamp(g.CurY+dt[1])
        g.CurE = True

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


#################### MAIN PART ####################

s = SenseHat()
s.clear()
g = Game()
s.stick.direction_any = handle_event

# Main game loop (watching for events and blink the cursor)
while not g.GameOver :
    g.curChange()
    time.sleep(0.5)

g.CurE = False
g.redraw()
time.sleep(3)
fadeAway()
s.show_message(f"{g.Steps} steps used.")

