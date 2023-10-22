#!/usr/bin/env python3
#################################################
# Raspberry Pi Sense Hat Maze
#

import random, sys, time, math
import sense_hat

TABLE    :dict = {}
SOLUTION :list = list(())

#################################################

class Game:

    def __init__(self, SizeX :int =-1, SizeY :int =-1) -> None:
        """Define a new playfield
        Parameters:
        SizeX :int = Horizontal size
        SizeY :int = Vertical size"""

        global TABLE
        self.SizeX :int = SizeX
        self.SizeY :int = SizeY
        self.V     :list = list(()) # This is the pixel vector to draw
        self.SpecCoord :dict = dict(()) # To store the coordinates of the special cells for distance computing

        # Create the cell objects
        for j in range(0,self.SizeY):
            for i in range(0,self.SizeX):
                TABLE[str(i)+","+str(j)] = Cell(i,j)
        # Limit the edges
        for j in range(0,self.SizeY):
            TABLE["0," + str(j)].allow["L"] = False
            TABLE[str(self.SizeX-1) + "," + str(j)].allow["R"] = False
        for i in range(0,self.SizeX):
            TABLE[str(i) + ",0"].allow["U"] = False
            TABLE[str(i) + "," + str(self.SizeY-1)].allow["D"] = False
        # Create a Start and an Exit
        sx = random.randint(1,SizeX//7)
        sy = random.randint(1,SizeY//7)
        if random.randint(0,100) > 50 : sx = SizeX-sx
        if random.randint(0,100) > 50 : sy = SizeY-sy
        ex = SizeX-sx ; ey = SizeY-sy
        self.StartCell = (sx,sy)
        self.EndCell   = (ex,ey)
        self.SpecCoord['E'] = (ex,ey)
        TABLE[str(ex)+","+str(ey)].makeSpecial('E')
        self.StartObj = TABLE[str(sx)+","+str(sy)]
        self.StartObj.makeSpecial('S')
        # Create the keys
        keyList = ['G','Y','R']
        while len(keyList) :
            k = keyList.pop()
            kx = random.randint(0,SizeX-1)
            ky = random.randint(0,SizeY-1)
            if TABLE[str(kx)+","+str(ky)].Special :
                keyList.append(k)
            else :
                TABLE[str(kx)+","+str(ky)].makeSpecial(k)
                self.SpecCoord[k] = (kx,ky)


    def redrawScreen(self, XOf :int =0, YOf :int =0) -> None:
        """Redraw the whole screen
        Parameters:
        XOf : The X offset of the map as int
        YOf : The Y offset of the map as int"""

        global TABLE
        for i in range(64) : self.V[i] = [0,0,0]

        #Walls come first: None, Visited, Route, Specials
        LS :list =list(())
        LR :list =list(())
        LV :list =list(())
        LN :list =list(())
        Dist :dict = dict(())
        for j in range(p.Y-2, p.Y+3):
            if j < 0 : continue
            if j >= self.SizeY : continue
            for i in range(p.X-2, p.X+3):
                if i < 0 : continue
                if i >= self.SizeX : continue
                co = TABLE[str(i)+","+str(j)]
                if co.Special :
                    LS.append([co,i,j])
                elif co.Route :
                    LR.append([co,i,j])
                elif co.Visited :
                    LV.append([co,i,j])
                else :
                    LN.append([co,i,j])
        for (co,i,j) in LN : co.draw( (i-p.X)*2+2+XOf , (j-p.Y)*2+3+YOf )
        for (co,i,j) in LV : co.draw( (i-p.X)*2+2+XOf , (j-p.Y)*2+3+YOf )
        for (co,i,j) in LR : co.draw( (i-p.X)*2+2+XOf , (j-p.Y)*2+3+YOf )
        for (co,i,j) in LS : co.draw( (i-p.X)*2+2+XOf , (j-p.Y)*2+3+YOf )

        #Status bars come second
        for i in range(8) : self.V[i] = [0,0,0]
        for i in range(7,64,8) : self.V[i] = [0,0,0]
        for (k,i,c1,c2) in [ ['R', 1, (240,0,0), (56,0,0)] , ['Y', 3, (220,220,0), (56,56,0)] , ['G', 5, (0,240,0), (0,56,0)] ] :
            self.V[i] = c1 if k in p.SpecList else c2

        #Next Artifact Radar on the right edge
        for i in ('R','Y','G','E') :
            Dist[i] = getDist(i)  # Measure the distances
            if i in p.SpecList :
                Dist[i] = 10000000.0   # Whatever we already have, ignore it by putting it virtually "far away"
        if len(p.SpecList) < 3 : Dist['E'] = 15000000.0  # If not having all the keys, Exit is unreachable
        Closest = 'X' ; CDist = 20000000.0  # Now check from the remaining items, which one is closest
        for i in ('R','Y','G','E') :
            if Dist[i] < CDist :
                CDist = Dist[i]
                Closest = i
        CDst = math.floor(CDist)
        BLen = 9-CDst
        if BLen < 0 : BLen = 0  # Bright Column Length
        DLen = 17-CDst
        if DLen < 0 : DLen = 0
        if DLen > 8 : DLen = 8  # Dark Column Length
        col = {'R':[48,0,0], 'G':[0,48,0], 'Y':[48,48,0], 'E':[48,0,48]}[Closest]
        if DLen :
            for i in range(DLen) :
                self.V[63-8*i] = col
        col = {'R':[248,0,0], 'G':[0,248,0], 'Y':[248,248,0], 'E':[248,0,248]}[Closest]
        if BLen :
            for i in range(BLen) :
                self.V[63-8*i] = col

        #Player gets drawn as last, to overwrite everything
        self.V[35] = [200, 200, 200]

        #Now draw everything on the screen
        s.set_pixels(self.V)



class Cell:

    def __init__(self, X :int =-1, Y :int =-1) -> None:
        """Define one cell element
        Parameters:
        X :int = X coordinate of the cell
        Y :int = Y coordinate of the cell"""

        self.X   :int = X
        self.Y   :int = Y
        self.Visited :bool =False
        self.Route   :bool =False
        self.Special :str  =None
        self.allow   :dict ={'U':True, 'D':True, 'L':True, 'R':True}

    def draw(self, wx :int, wy :int) -> None:
        """Add the cell to the desired position to the Pixel Vector.
        Parameters:
        wx :int = X coordinate of the top-left corner
        wy :int = Y coordinate of the top-left corner"""
        if wx in range(8) and wy in range(8) :
            g.V[wx+8*wy] = getWallColor(self.Special, self.Route, self.Visited)
        if wx+1 in range(8) and wy in range(8) :
            if self.allow['U'] :
                g.V[wx+1+8*wy] = [0,0,0]
            else :
                g.V[wx+1+8*wy] = getWallColor(self.Special, self.Route, self.Visited)
        if wx+2 in range(8) and wy in range(8) :
            g.V[wx+2+8*wy] = getWallColor(self.Special, self.Route, self.Visited)
        if wx in range(8) and wy+1 in range(8) :
            if self.allow['L'] :
                g.V[wx+8*wy+8] = [0,0,0]
            else :
                g.V[wx+8*wy+8] = getWallColor(self.Special, self.Route, self.Visited)
        if wx+1 in range(8) and wy+1 in range(8) :
            if self.Special and self.Special not in p.SpecList :
                g.V[wx+1+8*wy+8] = getArtifactColor(self.Special)
            else :
                g.V[wx+1+8*wy+8] = [0,0,0]
        if wx+2 in range(8) and wy+1 in range(8) :
            if self.allow['R'] :
                g.V[wx+2+8*wy+8] = [0,0,0]
            else :
                g.V[wx+2+8*wy+8] = getWallColor(self.Special, self.Route, self.Visited)
        if wx in range(8) and wy+2 in range(8) :
            g.V[wx+8*wy+16] = getWallColor(self.Special, self.Route, self.Visited)
        if wx+1 in range(8) and wy+2 in range(8) :
            if self.allow['D'] :
                g.V[wx+1+8*wy+16] = [0,0,0]
            else :
                g.V[wx+1+8*wy+16] = getWallColor(self.Special, self.Route, self.Visited)
        if wx+2 in range(8) and wy+2 in range(8) :
            g.V[wx+2+8*wy+16] = getWallColor(self.Special, self.Route, self.Visited)

    def visit(self) -> None:
        """Trigger the visited flag"""
        self.Visited = True

    def onroute(self) -> None:
        """Define the cell being on the final route"""
        self.Route = True

    def offroute(self) -> None:
        """Remove the cell from the route"""
        self.Route = False

    def makeSpecial(self, Artifact :str) -> None:
        """Change the cell to a special one.
        Parameters:
        Artifact :str = What is so special on this cell
        (accepted: S, E, R, Y, G)"""
        if Artifact[0].upper() in ['S', 'E', 'R', 'Y', 'G'] :
            self.Special = Artifact[0].upper()
        else :
            self.Special = None



class Player:

    def __init__(self, PosX :int =-1, PosY :int =-1) -> None:
        """Initialize a player with a given position and empty route
        Parameters:
        PosX :int = Horizontal position
        PosY :int = Vertical position"""
        self.X :int = PosX
        self.Y :int = PosY
        self.Route :list = list(())
        self.Won :bool =False
        self.SpecList :list = list(())

    def draw(self) -> None:
        """Draw the player to its appropriate position"""
        g.V[35] = [200, 200, 200]

    def step(self, Dir :str ="") -> None:
        """Try to step with the player into a certain direction
        Parameters:
        Dir :str = Stepping direction [U/D/L/R or N/S/W/E]"""

        global TABLE
        newX :int = self.X
        newY :int = self.Y
        currCell = TABLE[str(newX)+","+str(newY)]

        # apply direction
        if Dir.upper() in {"N","U"}: newY -= 1
        if Dir.upper() in {"S","D"}: newY += 1
        if Dir.upper() in {"W","L"}: newX -= 1
        if Dir.upper() in {"E","R"}: newX += 1

        # check if playfield limimts are reached
        if newX >= g.SizeX or newX < 0 or newY >= g.SizeY or newY < 0 : return

        # check if passable
        if not currCell.allow[Dir.upper()] : return

        # check if something special
        newCell = TABLE[str(newX)+","+str(newY)]
        if newCell.Special :
            if newCell.Special in ['R','Y','G'] and newCell.Special not in self.SpecList :
                self.SpecList.append(newCell.Special)
            if newCell.Special == 'E' and 'R' in self.SpecList and 'Y' in self.SpecList and 'G' in self.SpecList :
                self.Won = True

        # check if we are stepping on a cell with route, if yes then trim to the previous cell
        if newCell.Route :
            idx = self.Route.index(newCell)
            for id2 in range(idx, len(self.Route)) : self.Route[id2].offroute()
            self.Route = self.Route[0:idx]

        # mark current cell as visited and put new cell on the route
        currCell.visit()
        newCell.onroute()
        self.Route.append(newCell)

        # animate and step
        g.redrawScreen(self.X-newX,self.Y-newY)
        time.sleep(0.1)
        self.X , self.Y = newX , newY
        g.redrawScreen(0,0)



#################################################

def recurGenWalls(L: int, T: int, R: int, B: int) -> None:
    """Recursively generate walls by splitting the free rectangled areas
    Parameters:
    L :int = Leftmost cell of the area
    T :int = Top cell of the area
    R :int = Rightmost cell of the area
    B :int = Bottom cell of the area"""

    global TABLE

    Wid :int = abs(R-L+1)
    Hei :int = abs(B-T+1)
    if Wid == 1 or Hei == 1 : return

    if Wid >= Hei:
        splitX :int = random.randint(L, R-1)
        splitY :int = random.randint(T, B)
        for j in range(T, B+1):
            if j != splitY:
                TABLE[str(splitX)  +","+str(j)].allow["R"] = False
                TABLE[str(splitX+1)+","+str(j)].allow["L"] = False
        recurGenWalls(L, T, splitX, B)
        recurGenWalls(splitX+1, T, R, B)
    else:
        splitY :int = random.randint(T, B-1)
        splitX :int = random.randint(L, R)
        for i in range(L, R+1):
            if i != splitX:
                TABLE[str(i)+","+str(splitY)].allow["D"] = False
                TABLE[str(i)+","+str(splitY+1)].allow["U"] = False
        recurGenWalls(L, T, R, splitY)
        recurGenWalls(L, splitY+1, R, B)

def getArtifactColor(a: str) -> list :
    """Return the color of a specific artifact or feature.
    Parameters:
    a : Letter of the Artifact as str"""
    if not a : return [0,0,0]
    if a.upper() == "E" : return [240,0,240]
    if a.upper() == "R" : return [240,0,0]
    if a.upper() == "Y" : return [220,220,0]
    if a.upper() == "G" : return [0,240,0]
    return [0,0,0]

def getWallColor(s, r, v) -> list :
    """Return of a somewhat flickering color of the wall,
    depending if it is/was a room for an artifact,
    or has been visited already, or is on the currently shortest route.
    If an artifact has been picked, the room could be
    turned back to normal, but leaving it a special room
    with a special color helps the player to orientate.
    Parameters:
    s : Character of the Special artifact as str
    r : Whether the room is on the shortest route as bool
    v : Whether the room has been visited already as bool"""
    tlim = 110 if s else 60   # If special cell the wall colors get brighter
    blim = 80 if s else 48
    RC = random.randint(blim,tlim)
    GC = random.randint(blim,tlim)
    BC = random.randint(blim,tlim)
    if s :
        if s.upper() == 'R' :
            GC = 0 ; BC = 0
        elif s.upper() == "Y" :
            BC = 0
        elif s.upper() == "G" :
            RC = 0 ; BC = 0
        elif s.upper() == "E" :
            GC = 0
        elif s.upper() == "S" :
            RC = 0
    elif r :
        BC = 0
    elif v :
        BC = 0 ; RC = 0
    else :
        RC = 0 ; GC = 0

    return [RC, GC, BC]

def move_U(event) :
    if event.action=="pressed" : p.step('U')
def move_D(event) :
    if event.action=="pressed" : p.step('D')
def move_L(event) :
    if event.action=="pressed" : p.step('L')
def move_R(event) :
    if event.action=="pressed" : p.step('R')

def getDist(X :str) -> float :
    """Get the player's distance to a special cell.
    Parameters:
    X : the character of the artifact as str
    Returns : Distance in cells as float"""
    dx = p.X - g.SpecCoord[X][0]
    dy = p.Y - g.SpecCoord[X][1]
    ret :float = math.sqrt( dx*dx + dy*dy )
    return ret


#################################################


# Initial stuff
WID :int =20
HEI :int =20

# Generate map, initialize start and end, place player to the start
g = Game(WID,HEI)
recurGenWalls(0,0,WID-1,HEI-1)

p = Player(g.StartCell[0],g.StartCell[1])
p.Route.append(g.StartObj)

s = sense_hat.SenseHat()
s.clear()
g.V = s.get_pixels()
g.redrawScreen()

s.stick.direction_up = move_U
s.stick.direction_down = move_D
s.stick.direction_left = move_L
s.stick.direction_right = move_R


# Main loop
while not p.Won:
    time.sleep(0.1)


if p.Won :
    time.sleep(1)
    # Wait a little, then fade-out effect
    for i in range(40) :
        for j in range(64) :
            (rx,gx,bx) = g.V[j]
            rx = math.floor(rx*0.95) ; gx = math.floor(gx*0.95) ; bx = math.floor(bx*0.95)
            g.V[j] = [rx,gx,bx]
        s.set_pixels(g.V)
        time.sleep(0.1)
    s.clear()
    s.show_message("You have escaped !",text_colour=[0,255,0],back_colour=[0,48,0])
    time.sleep(1)

s.clear()
