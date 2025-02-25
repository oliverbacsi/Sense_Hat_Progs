#!/usr/bin/env python3
#################################################
# Four-in-a-row game for SenseHat
#

import random, time, math
try :
    from sense_hat import SenseHat
except :
    try :
        from sense_emu import SenseHat
    except :
        from _sense_hat_ANSI import SenseHat


#################### INIT PART ####################

# The 10 different colors (apart from white) to display
COLOROF :list = [(0,0,0), (220,0,0), (0,220,0), (0,0,200), (200,220,0), (0,130,230), (200,0,100), (200,100,0), (100,100,100), (120,0,230), (0,255,160), (255,255,255)]
RTCELLS :list = list(())

#################### CLASS PART ####################

class Cell :
    """Dummy Cell object for path optimization purposes"""

    def __init__(self, myIndex :int, boardValue :int) -> None :
        """Initialize a cell object for route optimization.
        :param myIndex: The cell index on the board: 0-63
        :param boardValue: The game board's value at the position of the cell
        :returns: List of neighbours that need updating."""
        self.myIndex    :int = myIndex
        self.boardValue :int = boardValue
        # Number of steps needed to reach me
        self.PathLength :int = 1000000
        # Have a valid path towards me
        self.CanReachMe :bool = False
        # Cell Object references to neighbours: Up,Down,Left,Right , Shortest_path
        self.Neighbour  :dict = { "U":None, "D":None, "L":None, "R":None, "S":None }

    def setNeighbour(self, Direction :str, NeighbourObject) -> bool :
        """Set up a neighbour object.
        :param Direction: Which neighbour it is, as single letter str
        :param NeighbourObject: The Object to refer to
        :returns: False if success, True if error"""
        if Direction not in ["U","D","L","R","S"] : return True
        self.Neighbour[Direction] = NeighbourObject
        return False

    def reset(self) -> None :
        """Reset attributes for a new search"""
        self.boardValue = g.Board[self.myIndex]
        self.PathLength = 1000000
        self.CanReachMe = False
        self.Neighbour["S"] = None

    def startMe(self) -> list :
        """Start the route on this cell.
        :returns: List of cells to be re-checked with reference to myself as caller"""
        self.PathLength = 0
        self.CanReachMe = True
        self.Neighbour["S"] = None
        retL :list = list(())
        for di in ["U","D","L","R"] :
            if self.Neighbour[di] : retL.append([self.Neighbour[di], self])
        return retL

    def processPath(self, whoCalled) -> list :
        """Process one step of the path on this cell.
        Evaluate if path can continue in my direction.
        :param whoCalled: Object reference to the previous cell on the route.
        :returns: List of cells to be re-checked with reference to myself as caller
        """
        # If I have value, cut things short
        if self.boardValue :
            self.PathLength = 1000000
            self.CanReachMe = False
            self.Neighbour["S"] = None
            return []

        # Only do something if caller has a better route than my current
        # If I didn't have route until now, the 1000000 is a worse route anyway
        if whoCalled.PathLength+1 >= self.PathLength : return []

        # Caller has a better path, so adjust to it
        self.PathLength = whoCalled.PathLength+1
        self.CanReachMe = True
        self.Neighbour["S"] = whoCalled

        # Tell the neighbours to update. Exclude the one who called me.
        # Although not excluding would also work as my route back to it
        # would result in a longer path length, so route would die anyway,
        # but it's more processing though.
        retL :list = list(())
        for di in ["U","D","L","R"] :
            if self.Neighbour[di] and self.Neighbour[di] != whoCalled :
                retL.append([self.Neighbour[di], self])
        return retL



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
        self.InjectBalls :int =3
        # The Game Field
        self.Board :list = [0] *64
        # Points earned
        self.Points :int =0
        # Is the game over?
        self.GameOver :bool =False
        # Cursor Position, Enablement and On Status
        self.cP :int =0
        self.cE :bool =True
        self.cS :bool =True
        # In case a ball is already selected to move:
        # *Being in "Selected Mode"
        self.selMode :bool =False
        # *Selected Ball's Position and Color
        self.selP :int =-1
        self.selC :int =-1
        # *The "route" to display, excluding start and end:
        self.selRoute :list =list(())
        # *A helper variable to indicate whether a valid path exists.
        #  This is set only by the getPath method,
        #  but can be used by anyone.
        self.validRoute :bool =False

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

    def dropNewBalls(self) -> None :
        """Inject some new random color balls into the playfield"""
        self.checkGameOver()
        if self.GameOver : return
        # Disable cursor blink and regen screen
        self.cE = False ; self.cS = False ; self.redrawScreen()
        EmptyPositions :list = list(())
        for xx in range(64) :
            if not self.Board[xx] : EmptyPositions.append(xx)
        for yy in range(self.InjectBalls) :
            vv = random.choice(EmptyPositions)
            self.Board[vv] = random.randint(1,self.NumColor)
            EmptyPositions.remove(vv)
            # Give one point of score for each ball that could be injected
            self.Points += 1
            self.redrawScreen()
            time.sleep(0.3)
        self.cE = True

    def checkAndRemove(self) -> None :
        """Check ball under current position and determine removable
        balls with similar color in all 8 directions"""
        # OK, actually these are only 4 directions:
        # 0=North-South, 1=NE-SW, 2=E-W, 3=NW-SE

        # Let's store which position the Cursor is in
        Pos :int = self.cP
        # And what value is under the Cursor
        PickedColor :int = self.Board[Pos]
        # Just in case this is invoked on an empty cell:
        if not PickedColor : return
        # Collect the list of removable positions in each 4 directions.
        # Remember: opposite directions are the same and count to the same
        # row of equal colored balls !
        Removables :list = [ [Pos], [Pos], [Pos], [Pos] ]

        # Go in each 8 direction and append the positions that are adjacent
        # and contain the same colored ball.
        # Going North or South both count to direction '0' though
        for (Direction, Delta) in [ (0,-8), (1,-7), (2,1), (3,9), (0,8), (1,7), (2,-1), (3,-9) ] :
            i = Pos + Delta
            while i in range(64) and self.Board[i] == PickedColor :
                Removables[Direction].append(i) ; i += Delta

        # Now all the 4 elements of the Removables list is a list itself,
        # containing the removable balls in one direction
        # Let's see first if it is a combo, to give more points.
        # Let the rule be:
        # - If there is only one direction, then one ball is 10 pts
        # - If two directions apply, one ball should be 20 pts, as a combo bonus
        # - etc
        # - The ball in the 'Pos' should not be counted multiple times though
        NumCombo :int =0
        # So if one direction does not meet the minimum number of balls, skip it.
        for Direction in range(4) :
            if len(Removables[Direction]) < self.FullRow :
                Removables[Direction] = []
            else :
                NumCombo += 1

        # If none of the directions met, we punish the player with adding balls
        if not NumCombo :
            time.sleep(0.3)
            self.dropNewBalls()
            return

        # Add up the score first
        self.Points += NumCombo*10*(len(Removables[0])+len(Removables[1])+len(Removables[2])+len(Removables[3]))-NumCombo+1
        # Now light up all removed balls
        # Disable cursor blink and regen screen
        self.cE = False ; self.cS = False ; self.redrawScreen()
        for Direction in range(4) :
            for i in Removables[Direction] :
                self.Board[i] = 11
        self.redrawScreen()
        time.sleep(0.8)
        for Direction in range(4) :
            for i in Removables[Direction] :
                self.Board[i] = 0
        self.redrawScreen()
        self.cE = True

    def unselect(self) -> None :
        """Convenience method to reset all selection attributes"""
        self.selMode = False
        self.selC = 0
        self.selP = -1
        self.selRoute = list(())
        self.validRoute = False

    def handleEnter(self) -> None :
        """Handle the Enter key (or middle click).
        If not in 'Selected Mode' : check if a ball can be selected, and select it.
        If in 'Selected Mode' :
        - If the same ball is clicked, then leave 'Selected Mode'.
        - If an empty location is clicked, then perform the move if there is a free path.
        Return value is not needed as no error can occur, the output is seen on the screen."""
        global COLOROF

        # If a ball has been selected already:
        if self.selMode :

            # The previously selected ball is clicked again
            if self.selP == self.cP : self.unselect()

            # An empty place is clicked, so try to move the ball
            else :
                if self.validRoute :
                    # Animate ball all the way down the route
                    self.Board[self.selP] = 0
                    for pos in self.selRoute :
                        self.Board[pos] = self.selC
                        self.redrawScreen()
                        time.sleep(0.1)
                        self.Board[pos] = 0
                    self.Board[self.cP] = self.selC
                    # Finished animation, redraw screen
                    self.redrawScreen()
                    # Check if the ball creates removable rows in its new position
                    self.checkAndRemove()
                    # If nothing removed but new balls added but screen is ful
                    if self.GameOver : return
                    self.unselect()

        # Currently not in 'Selected Mode', so let's see if we can select something
        else :
            ClickedBall = self.Board[self.cP]

            # There is something under the cursor
            if ClickedBall :
                self.selMode = True
                self.selC = ClickedBall
                self.selP = self.cP
                self.selRoute = list(())
                self.validRoute = False

            # Nothing is under the cursor
            else :
                self.unselect()

    def blinkCursor(self) -> None :
        """Blink the cursor. Sounds simple. BUT:
        * in cruising mode blink a single white dot
        * in selection mode blink the whole route"""
        global COLOROF

        # Cursor blinking not enabled:
        if not self.cE : return

        # If cursor "not lit", just erase all crap and show the game field
        self.redrawScreen()
        if not self.cS :
            self.cS = True
            return

        # If in selection mode and the path is valid, then try to draw it
        if self.selMode and self.validRoute :
            for pos in self.selRoute :
                s.set_pixel(pos%8,pos//8,(65,65,65))

        # Now the actual cursor with bright white
        s.set_pixel(self.cP%8,self.cP//8,(255,255,255))

        # Now invert the status (to make it blink)
        self.cS = not self.cS

    def findRoute(self) -> None :
        """Try to find a route between the selected ball and the crsr.
        Only empty target cells are OK.
        Diagonal travelling is not allowed, a diagonal row of balls is a wall.
        """
        global RTCELLS
        self.selRoute = list(())
        self.validRoute = False
        if not self.selMode : return

        # If crsr is standing over the selected ball, theoretically the route is OK,
        # but since this is used to cancel the selection, let's invalidate it
        if self.cP == self.selP : return

        # If cell under cursor is not empty, the route is NOT OK
        if self.Board[self.cP] : return

        # All 4 adjacent cells are valid route with no route list
        # Remove adjacency if being on one of the vertical edges
        ChkDiffs :set = set((-8, -1, 1, 8))
        if self.cP %8 == 0 : ChkDiffs.discard(1)
        if self.cP %8 == 7 : ChkDiffs.discard(-1)
        if self.cP-self.selP in ChkDiffs :
            self.validRoute = True
            return

        # Now we know we need to find a route to a non-adjacent empty cell
        # Initialize 64 cell objects for recursive path search
        for co in RTCELLS : co.reset()
        # List of cell IDs to need to work on
        NeedProcessing :list = RTCELLS[self.selP].startMe()

        # While there are cells to process, then process them,
        # until all the cells are settled down with their values
        while len(NeedProcessing) :
            Next = NeedProcessing.pop(0)
            NeedProcessing.extend(Next[0].processPath(Next[1]))

        # Now check if the cell under the cursor is reachable at all
        if not RTCELLS[self.cP].CanReachMe : return

        # Now trace backwards the neighbours with the shortest route
        obj = RTCELLS[self.cP].Neighbour["S"]
        while obj :
            self.selRoute.append(obj.myIndex)
            obj = obj.Neighbour["S"]
        # Reverse the list to get a forward route
        self.selRoute.reverse()
        # Since the starting cell is also in this route, cut it off
        self.selRoute = self.selRoute[1:]
        self.validRoute = True



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

def move_C(event) :
    if event.action=="pressed" : g.handleEnter()
def move_U(event) :
    if event.action!="pressed" : return
    g.cE = False ; g.cS = False ; g.redrawScreen()
    if g.cP-8 in range(64) : g.cP -= 8
    if g.selMode : g.findRoute()
    g.cE = True ; g.cS = True ; g.blinkCursor()
def move_D(event) :
    if event.action!="pressed" : return
    g.cE = False ; g.cS = False ; g.redrawScreen()
    if g.cP+8 in range(64) : g.cP += 8
    if g.selMode : g.findRoute()
    g.cE = True ; g.cS = True ; g.blinkCursor()
def move_L(event) :
    if event.action!="pressed" : return
    g.cE = False ; g.cS = False ; g.redrawScreen()
    if g.cP-1 in range(64) : g.cP -= 1
    if g.selMode : g.findRoute()
    g.cE = True ; g.cS = True ; g.blinkCursor()
def move_R(event) :
    if event.action!="pressed" : return
    g.cE = False ; g.cS = False ; g.redrawScreen()
    if g.cP+1 in range(64) : g.cP += 1
    if g.selMode : g.findRoute()
    g.cE = True ; g.cS = True ; g.blinkCursor()


#################### MAIN PART ####################

s = SenseHat()
s.clear()
s.stick.direction_up = move_U
s.stick.direction_down = move_D
s.stick.direction_left = move_L
s.stick.direction_right = move_R
s.stick.direction_middle = move_C

g = Game()
g.dropNewBalls()
g.redrawScreen()

for cl in range(64) : RTCELLS.append(Cell(cl,g.Board[cl]))
for cl in range(64) :
    if cl >  7 : RTCELLS[cl].setNeighbour("U",RTCELLS[cl-8])
    if cl < 56 : RTCELLS[cl].setNeighbour("D",RTCELLS[cl+8])
    if cl%8    : RTCELLS[cl].setNeighbour("L",RTCELLS[cl-1])
    if cl%8 <7 : RTCELLS[cl].setNeighbour("R",RTCELLS[cl+1])

g.cE = True

while not g.GameOver :
    g.blinkCursor()
    time.sleep(0.15)
    if not g.cS : time.sleep(0.3)

time.sleep(2)
fadeAway()
s.show_message(f"GAME OVER. Points: {g.Points}")

s.clear()

