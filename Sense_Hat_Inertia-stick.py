#!/usr/bin/env python3
##########################################
# Inertia Game
#

# Technical stuff:

# Direction vector coding: up=0, turning 45 deg towards right is +1, so east=2, south=4
# 7 0 1
# 6 + 2
# 5 4 3


#################### INIT PART ####################

import random, time, math
import sense_hat

COLOROF :dict = {'b':[0,0,48], 'w':[65,65,65], 'g':[0,220,80], 'm':[220,0,0], 'S':[0,0,48], 's':[48,48,0], '@':[255,255,255]}

#################### CLASS PART ####################

class Game :
    """Stores general game parameters"""

    def __init__(self) :
        # List of 64 Cell objects:
        self.Grid :list = list(())
        # Player's coordinates
        self.pX :int =-1
        self.pY :int =-1
        # Looking direction of player
        self.pD :int =-1
        # Game starting coordinates
        self.sX :int =-1
        self.sY :int =-1
        # Cursor coordinates, Enablement and On Status
        self.cX :int =-1
        self.cY :int =-1
        self.cE :bool =True
        self.cS :bool =True
        # Number of gems so that game over can be tracked
        self.NumGems :int =-1
        # Game status: 'r'-running 's'-solved 'd'-dead
        self.Status :str ='r'

        # Service variables
        # Possible positions
        self.positions :list = []


    def _can_go(self, x1: int, y1 :int, d1 :int, x2 :int, y2 :int, d2 :int) -> bool :
        """Check if we can go from (x1,y1) direction d1 to (x2,y2) direction d2"""
        xn :int = x1+dX(d1)
        yn :int = y1+dY(d1)

        # If we are standing on a wall or mine, no move is possible
        Here :str = self.Grid[x1+y1*8].Content
        if Here in ['w', 'm'] : return False

        # If we are capable to stop at x1,y1 then we can change direction so it is true
        if xn in range(8) and yn in range(8) :
            Next :str = self.Grid[x1+dX(d1)+(y1+dY(d1))*8].Content
        else :
            Next :str = 'w'
        if x2 == x1 and y2 == y1 and (Here in ['s', 'S'] or Next =='w') : return True

        # If we are capable to move 1 step and the direction is the same, then step
        There :str = self.Grid[x2+y2*8].Content
        if x2 == xn and y2 == yn and d2 == d1 and There in ['b', 'g', 's', 'S'] : return True

        return False


    def _find_gem_candidates(self) -> int :
        """Finds all cells which are good candidates for a gem.
        Candidate cells should be reachable from the start and
        start should be reachable from the candidate cell.
        Grid has no gems but empty cells, trying to find which can be gems."""
        possgems :int
        for sign in [1, -1] :
            head =0 ; tail =0

            for _dir in range(8) :
                if sign > 0 :
                    self.Grid[self.sX+8*self.sY].reachable_from[_dir] = True
                else :
                    self.Grid[self.sX+8*self.sY].reachable_to[_dir] = True
                self.positions.append((self.sX, self.sY, _dir))
                tail +=1

            while head < tail :
                _x, _y, _dir = self.positions[head]
                head +=1

                for n in range(-1,8) :
                    if n<0 :
                        _x2 = _x + sign* dX(_dir)
                        _y2 = _y + sign* dY(_dir)
                        _d2 = _dir
                    else :
                        _x2 = _x ; _y2 = _y ; _d2 = n
                    if _x2 not in range(8) or _y2 not in range(8) : continue
                    if sign > 0 :
                        _r = self.Grid[_x2+8*_y2].reachable_from[_d2]
                    else :
                        _r = self.Grid[_x2+8*_y2].reachable_to[_d2]
                    if _x2 in range(8) and _x2 in range(8) and not _r :
                        if sign > 0 :
                            ok = self._can_go(_x, _y, _dir, _x2, _y2, _d2)
                        else :
                            ok = self._can_go(_x2, _y2, _d2, _x, _y, _dir)
                        if ok :
                            self.positions.append((_x2, _y2, _d2))
                            tail +=1
                            if sign > 0 :
                                self.Grid[_x2+8*_y2].reachable_from[_d2] = True
                            else :
                                self.Grid[_x2+8*_y2].reachable_to[_d2] = True

        possgems =0
        for gy in range(8) :
            for gx in range(8) :
                if self.Grid[gx+8*gy].Content == 'b' :
                    for gd in range(8) :
                        if self.Grid[gx+8*gy].reachable_from[gd] and self.Grid[gx+8*gy].reachable_to[gd] :
                            self.Grid[gx+8*gy].Content = 'p'
                            possgems += 1
                            break

        return possgems


    def genGrid(self) -> None :
        """Generate a new playfield"""
        MAXDIST :int =2
        TRIES :int =0

        while True :
            # Add 12 elements each from Wall, Stop, Mine, a start and blanks
            ElemList = list('w')*12 + list('s')*12 + list('m')*12 + list('S') + list('b')*27
            self.Grid = [] ; self.positions = []
            for i in range(64) :
                self.Grid.append(Cell())
                self.Grid[-1].Content = ElemList.pop(random.randint(0,len(ElemList)-1))
                if self.Grid[-1].Content == 'S' :
                    self.sX = i%8
                    self.sY = int(i/8)
                    self.pX = self.sX ; self.pY = self.sY
                    self.cX = self.sX ; self.cY = self.sY

            possgems = self._find_gem_candidates()
            # If the number of possible gems is less than 20% of the playfield then re-do
            if possgems < 12 : continue

            _dist = [-1]*64
            _list = list(())
            head =0 ; tail =0
            for i in range(64) :
                if self.Grid[i].Content == 'p' :
                    _dist[i] =0
                    _list.append(i)
                    tail +=1
            maxdist =0

            while head < tail :
                pos = _list[head]
                head +=1
                maxdist = max(maxdist, _dist[pos])
                x = pos%8 ; y = int(pos/8)

                for d in range(8) :
                    x2 = x + dX(d) ; y2 = y + dY(d)
                    if x2 in range(8) and y2 in range(8) :
                        p2 = y2*8+x2
                        if _dist[p2] < 0 :
                            _dist[p2] = _dist[pos]+1
                            _list.append(p2)
                            tail +=1

            # Check if possible gems are available from the
            # reachable cells with not more than MAXDIST steps.
            # Retry 30 times, and start loosen the requirements...
            if maxdist > MAXDIST :
                TRIES += 1
                if TRIES >= 30 :
                    TRIES = 0
                    MAXDIST += 1
                continue

            # Fill only max 12 of possible gems with real gems
            _list2 = list(())
            for i in range(64) :
                if self.Grid[i].Content == 'p' : _list2.append(i)
            i =0
            while len(_list2) :
                p = _list2.pop(random.randint(0,len(_list2)-1))
                self.Grid[p].Content = 'g' if i<12 else 'b'
                i +=1
            self.NumGems = 12
            self.Status = 'r'
            self.pD = -1
            break


    def redrawGrid(self) -> None :
        """Redraw the 8x8 LED screen based on the game status"""
        global COLOROF
        Vector :list = list(())
        for pos in range(64) :
            Vector.append(COLOROF[self.Grid[pos].Content])
        s.set_pixels(Vector)
        s.set_pixel(self.pX, self.pY, COLOROF['@'])


    def redrawPix(self, x :int, y :int, blank :bool =False) -> None :
        """Redraw one pixel on the screen, considering cursor blinking:
        Parameters:
        :param x : the x coordinate of the pixel
        :param y : the y coordinate of the pixel
        :param blank : if the cursor is active, pixel should be blanked, otherwise show its own color
        :returns : None"""
        global COLOROF
        if blank :
            _col = [0,0,0]
        else :
            if x == self.pX and y == self.pY :
                _col = COLOROF['@']
            else :
                _col = COLOROF[self.Grid[8*y+x].Content]
        s.set_pixel(x, y, _col)

    def animatePlayer(self) -> None:
        """Animate the step on the screen"""
        dx = self.cX-self.pX ; dy = self.cY-self.pY
        while True :
            newx = self.pX + dx ; newy = self.pY + dy
            # Check if we hit the edge of the screen
            if newx not in range(8) or newy not in range(8) : break
            nextItem = self.Grid[8*newy+newx].Content
            # Check if we hit a wall
            if nextItem == 'w' : break

            # So now we are able to step, so let's step
            self.pX = newx ; self.pY = newy
            self.redrawGrid() ; time.sleep(0.5)

            # If we stepped on a mine then die
            if nextItem == 'm' :
                self.Status = 'd'
                break
            # If we stepped on a gem, then collect it
            if nextItem == 'g' :
                self.Grid[8*newy+newx].Content = 'b'
                self.NumGems -=1
            # If we are on a stopper then stop
            if nextItem == 's' : break
            # In any other case just let the "while True" run and do one more step

        # Adjust cursor position to player position
        self.cX = self.pX ; self.cY = self.pY ; self.pD = -1



class Cell :
    """Stores the data for one cell"""

    def __init__(self) :
        # What is in the cell?
        # 'b'-blank 'g'-gem 'm'-mine 's'-stop 'S'-Start 'w'-wall 'p'-possible_gem
        self.Content :str ='b'

        # Service variables
        # Reachable from the start, by direction
        self.reachable_from :list = [False, False, False, False, False, False, False, False]
        # Start is reachable from here, by direction
        self.reachable_to :list = [False, False, False, False, False, False, False, False]



#################### PROC PART ####################


def dX(_dir: int) -> int :
    """Return the delta-X value for a direction.
    Parameters:
    :param _dir : The direction vector number.
    :returns : [-1, 0, 1]"""
    if _dir < 0 : return 0
    if _dir % 4 :
        if _dir > 4 :
            return -1
        else :
            return 1
    return 0

def dY(_dir: int) -> int :
    """Return the delta-Y value for a direction.
    Parameters:
    :param _dir : The direction vector number.
    :returns : [-1, 0, 1]"""
    if _dir < 0 : return 0
    return dX((_dir+6)%8)

def clamp(Value :int, _minVal :int =0, _maxVal :int =7) -> int :
    return max(min(Value,_maxVal),_minVal)

def handleEvent(event) -> None :
    """Handle the stick events
    Parameters:
    :param event : The stick event"""
    if event.action != "pressed" : return
    g.cE = False ; g.cS = False
    g.redrawGrid()

    if event.direction == "middle" :
        if g.pD < 0 :
            g.cE = True
            return   # Player clicked on him/herself
        g.animatePlayer()
        g.redrawGrid()
        g.cE = True
    else :
        dt = {"up":(0,-1) , "down":(0,1) , "left":(-1,0) , "right":(1,0)}[event.direction]
        g.cX = clamp(clamp(g.cX+dt[0],g.pX-1,g.pX+1),0,7)
        g.cY = clamp(clamp(g.cY+dt[1],g.pY-1,g.pY+1),0,7)
        g.pD = [(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,0)].index((g.cX-g.pX,g.cY-g.pY))
        if g.pD == 8 : g.pD = -1
        g.redrawGrid()
        g.cE = True

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


s = sense_hat.SenseHat()
s.clear()

g = Game()
g.genGrid()
g.redrawGrid()
s.stick.direction_any = handleEvent


while g.Status == 'r' :
    # Basically blink the cursor...
    if g.cE :
        g.cS = not g.cS
        g.redrawPix(g.cX, g.cY, g.cS)
        # We are checking this here to make sure we are in "idle" mode with the player standing.
        if g.NumGems < 1 and g.Status != 'd' : g.Status = 's'
    time.sleep(0.5)


if g.Status == 'd' :
    for z in range(3) :
        s.clear([255,100,100])
        time.sleep(0.3)
        s.clear()
        time.sleep(0.3)
    g.redrawGrid()
    time.sleep(3)
    fadeAway()
    s.show_message("You stepped on a mine!",text_colour=[255,100,100],back_colour=[48,0,0])
else :
    s.clear([0, 220, 80])
    time.sleep(1)
    g.redrawGrid()
    time.sleep(3)
    fadeAway()
    s.show_message("You won!",text_colour=[100,255,100],back_colour=[0,48,0])

s.clear()
