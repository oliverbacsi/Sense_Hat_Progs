#!/usr/bin/env python3
#################################################
# The classic Color Flood game for Sense Hat
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


# For the cells to display we need to have at least 11 different colors.
# To be on the safe side let's define 12 colors.
# Since each cell will be displayed on 2x2 pcs of LEDs, so the "shape" to display
# can be the binary representation of the value of the cell, like
# 1 = first pixel lit, 15 = all 4 pixels lit.
# Values over 15 can not be displayed but this is way over the goal of the game,
# as it goes only until reaching 2^11
# ColorH is the color of the brighter pixel in the pattern,
# ColorL is the color of the darker pixel in the pattern
COLORH :list = [(0,0,0), (100,100,100), (255,0,60), (255,120,0), (255,255,0), (0,200,0), (0,200,255), ( 0, 0,255), (140,0,240), (255,100,180), (220,220,220), (255,255,255), (255,255,255)]
COLORL :list = [(0,0,0), ( 48, 48, 48), (100,0,60), (155, 60,0), (155,155,0), (0,100,0), (0,100,155), ( 0, 0,155), ( 70,0,120), (155, 65, 90), (110,110,110), (155,155,155), (255,255,255)]


#################### CLASS PART ####################


class Game :

    def __init__(self) :
        """Initialize the game parameters"""

        # This list stores the 4x4 board, starting from the top-left corner,
        # going to the right end of top row first, then one row down and start from left again.
        # The value stored: is the power of 2.
        # As in the game there is no "1" ever, everything starts from "2",
        # So it is safe to choose "0" for the empty cell, as 2^0 = 1, and this never appears,
        # And it is easy to check the presence of any value using if(BOARD[...])
        # Values begin with 1 , meaning 2^1 = 2
        # Highest score to achieve is 2048, which is 2^11 , so cell value 11.
        # If 2048 is reached, the user can get a celebration.
        # Otherwise if game is lost earlier, the score can be the sum of the values,
        # i.e.: Sum(2^x) for each x = BOARD[0...15]
        self.BOARD :list = [0]*16

        # 0 while in game
        # -1 if lost
        # +1 if won
        self.GameStatus :int =0

        # This has not too much meaning, but just for fun:
        self.NumTurns :int =0


    def redraw(self) -> None :
        """Redraw the screen based on the board data"""
        global COLORH, COLORL
        # For each of the 16 cells get the X-Y coordinate and value
        # Select the bright and dim pixel colors accordingly
        for i in range(16) :
            X = (i%4)*2 ; Y = (i//4)*2 ; V=self.BOARD[i]
            CH = COLORH[V] ; CL = COLORL[V]
            s.set_pixel(X  , Y  , CH if V&8 else CL)
            s.set_pixel(X+1, Y  , CH if V&4 else CL)
            s.set_pixel(X  , Y+1, CH if V&2 else CL)
            s.set_pixel(X+1, Y+1, CH if V&1 else CL)


    def dropNewNumber(self) -> bool :
        """Drop a '2' value into a random empty position
        :returns: False if success, True if failure
        So this implicitly performs the game-over-check as well"""
        EmptyCells :list =list(())
        # Collect the list of indexes of empty cells
        for i in range(16) :
            if not self.BOARD[i] :
                EmptyCells.append(i)
        # If no any, BUT we are not at the point when the players makes a move,
        # but we are trying to add an additional number but there is no place,
        # so this is the Game Over condition.
        if not len(EmptyCells) :
            self.GameStatus = -1
            return True
        # So we have at least one emply place to occupy. Let's pick one.
        pos = random.choice(EmptyCells)
        self.BOARD[pos]=1
        self.redraw()
        return False


    def move(self, Direction :str) -> None :
        """Handle the keypress, so try to move the board in a certain direction.
        Implicitly handle the merging of the numbers to the higher power as well.
        Implicitly check for the game won (reaching 2048).
        :param Direction: 'L','R','U','D' indicating the direction.
        This method always succeeds, even if no numbers were moved,
        so as for now, no return value is needed."""

        # First of all it needs to be decided if we allow multiple merging in one turn,
        # or just one merge per move???
        # What does it mean :
        # - Single merge per turn:
        # A row looks like this :  2 2 4 8   Then pressing "Left" causes:
        # 4 4 8 _   ; then it needs one more "Left" move to get to:
        # 8 8 _ _   ; then it needs one more "Left" move to get to:
        # 16 _ _ _  ; So one merge per game turn, there is no "combo"
        # - If multiple merges are allowed per turn,
        # then we get straight to the "16" in one turn,
        # as the algorhythm goes as long as there is something to merge
        # For now, let's only enable unlimited sliding but only 1 merge for 1 number.
        # Therefore the following variable is needed to remember which position
        # has been merged already during 1 turn.
        # If unlimited merges are allowed, this watchdog has to be disabled.
        MergedPositions :set = set(())

        # To store if something has changed in one turn.
        # If not, all movements are stopped already.
        SomethingChanged :bool =True

        Direction = Direction.strip().upper()[0]

        if Direction == 'L' :
            while SomethingChanged :
                SomethingChanged = False
                for dx in range(1,4) :
                    for dy in range(4) :
                        idx = dx + 4*dy
                        # If no value here, then skip
                        if not self.BOARD[idx] : continue
                        # So, there is value here where we stand, let's check if
                        # the neighbouring cell is free so that we can step
                        if not self.BOARD[idx-1] :
                            self.BOARD[idx-1] = self.BOARD[idx]
                            self.BOARD[idx] = 0
                            SomethingChanged = True
                            continue
                        # So there is something in the neighbouring cell as well
                        # Let's check if it is equal to myself
                        # AND if it has not been merged already then merge and mark
                        if self.BOARD[idx-1] == self.BOARD[idx] :
                            if idx-1 not in MergedPositions and idx not in MergedPositions :
                                self.BOARD[idx-1] += 1
                                self.BOARD[idx] = 0
                                MergedPositions.add(idx-1)
                                SomethingChanged = True
                self.redraw()
                time.sleep(0.1)

        elif Direction == 'R' :
            while SomethingChanged :
                SomethingChanged = False
                for dx in range(2,-1,-1) :
                    for dy in range(4) :
                        idx = dx + 4*dy
                        # If no value here, then skip
                        if not self.BOARD[idx] : continue
                        # So, there is value here where we stand, let's check if
                        # the neighbouring cell is free so that we can step
                        if not self.BOARD[idx+1] :
                            self.BOARD[idx+1] = self.BOARD[idx]
                            self.BOARD[idx] = 0
                            SomethingChanged = True
                            continue
                        # So there is something in the neighbouring cell as well
                        # Let's check if it is equal to myself
                        # AND if it has not been merged already then merge and mark
                        if self.BOARD[idx+1] == self.BOARD[idx] :
                            if idx+1 not in MergedPositions and idx not in MergedPositions :
                                self.BOARD[idx+1] += 1
                                self.BOARD[idx] = 0
                                MergedPositions.add(idx+1)
                                SomethingChanged = True
                self.redraw()
                time.sleep(0.1)

        elif Direction == 'U' :
            while SomethingChanged :
                SomethingChanged = False
                for dy in range(1,4) :
                    for dx in range(4) :
                        idx = dx + 4*dy
                        # If no value here, then skip
                        if not self.BOARD[idx] : continue
                        # So, there is value here where we stand, let's check if
                        # the neighbouring cell is free so that we can step
                        if not self.BOARD[idx-4] :
                            self.BOARD[idx-4] = self.BOARD[idx]
                            self.BOARD[idx] = 0
                            SomethingChanged = True
                            continue
                        # So there is something in the neighbouring cell as well
                        # Let's check if it is equal to myself
                        # AND if it has not been merged already then merge and mark
                        if self.BOARD[idx-4] == self.BOARD[idx] :
                            if idx-4 not in MergedPositions and idx not in MergedPositions :
                                self.BOARD[idx-4] += 1
                                self.BOARD[idx] = 0
                                MergedPositions.add(idx-4)
                                SomethingChanged = True
                self.redraw()
                time.sleep(0.1)

        elif Direction == 'D' :
            while SomethingChanged :
                SomethingChanged = False
                for dy in range(2,-1,-1) :
                    for dx in range(4) :
                        idx = dx + 4*dy
                        # If no value here, then skip
                        if not self.BOARD[idx] : continue
                        # So, there is value here where we stand, let's check if
                        # the neighbouring cell is free so that we can step
                        if not self.BOARD[idx+4] :
                            self.BOARD[idx+4] = self.BOARD[idx]
                            self.BOARD[idx] = 0
                            SomethingChanged = True
                            continue
                        # So there is something in the neighbouring cell as well
                        # Let's check if it is equal to myself
                        # AND if it has not been merged already then merge and mark
                        if self.BOARD[idx+4] == self.BOARD[idx] :
                            if idx+4 not in MergedPositions and idx not in MergedPositions :
                                self.BOARD[idx+4] += 1
                                self.BOARD[idx] = 0
                                MergedPositions.add(idx+4)
                                SomethingChanged = True
                self.redraw()
                time.sleep(0.1)

        else : return

        # Check if game is won.
        # If only 1 merge is allowed per turn, then after the maximum value of 10
        # there can be only 11 in the next turn, so it would be enough to check:
        #   if 11 in self.BOARD :    ....
        # But if multiple merges are allowed per turn, then theoretically
        # there can be even a 12:
        # 10 10 10 10  -->  12 _ _ _
        # So let's do this way :
        if max(self.BOARD) > 10 : self.GameStatus = 1

        self.NumTurns += 1

        # It's better to put dropping the new number here,
        # As this is the point where we could check that a valid move was made
        # Even if it is against the wall, so nothing happened on the board
        # If the game is already won, don't try to add a new number,
        # just to realize that it failed, and then changing the
        # win result to a fail
        if not self.GameStatus : self.dropNewNumber()


#################### PROC PART ####################


def move_U(event) :
    if event.action=="pressed" : g.move('U')
def move_D(event) :
    if event.action=="pressed" : g.move('D')
def move_L(event) :
    if event.action=="pressed" : g.move('L')
def move_R(event) :
    if event.action=="pressed" : g.move('R')
def endGame(event) :
    if event.action=="pressed" : g.GameStatus = -1

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
s.stick.direction_up = move_U
s.stick.direction_down = move_D
s.stick.direction_left = move_L
s.stick.direction_right = move_R
s.stick.direction_middle = endGame
g = Game()

# Initially put two numbers somewhere
g.dropNewNumber() ; g.dropNewNumber()


# Main loop goes here, stay in the loop while no game over
while not g.GameStatus :
    # To avoid multiple key detections:
    # Get the list of events, take the first item, throw away the rest.
    time.sleep(0.1)


# If game has ended by losing:
if g.GameStatus < 0 :
    time.sleep(0.3)
    fadeAway()
    Sum :int =0
    for zs in range(16) :
        if g.BOARD[zs] :
            Sum += 2**g.BOARD[zs] * g.BOARD[zs]
    s.show_message(f"GAME OVER after {g.NumTurns} turns, total score: {Sum}",text_colour=[255,100,100],back_colour=[48,0,0])
# If game has ended by winning:
else :
    time.sleep(0.3)
    fadeAway()
    s.show_message(f"YOU REACHED 2048 in {g.NumTurns} turns",text_colour=[100,255,100],back_colour=[0,48,0])


s.clear()

