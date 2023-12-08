#!/usr/bin/env python3
###########################################
# The classic Reversi game for Sense Hat


#################### INIT PART ####################

import time
try :
    from sense_hat import SenseHat
except :
    try :
        from sense_emu import SenseHat
    except :
        from _sense_hat_ANSI import SenseHat

# The original game has Black and White tiles, Black begins the game.
# But since on the Sense Hat it's hard to display Black tiles
# (may be the whole background is grey -- but still looks quite strange
# as the black tiles appear as "burnt out LEDs", so not a good option)
# so here we re-define the colors the following way:
# Player = Originally Black --> Blue here
# Computer = Originally White --> Red here
# But not to confuse the coder, all variables in the code still remain
# to refer to "Black", "White", "B", "W", etc
# Change the below color mapping to any arbitrary You like:
# "W1" is the color of the White tiles when highlighted and
# "B0" is the color of the Black tiles when not highlighted, the rest You get by Yourself
COLOR :dict = {"W1":[255,0,0], "W0":[120,0,0], "B1":[0,0,255], "B0":[0,0,120]}

# Advanced weightage, this is the default "Value" of the cells
# that count as a gain when the solver algorhythm gets them,
# and as a loss if the human player gets them.
# This helps the solver algorhythm to pick the best option for the computer move.
WEIGHTS = [[10000, -3000, 1000,  800,  800, 1000, -3000, 10000],
           [-3000, -5000, -450, -500, -500, -450, -5000, -3000],
           [ 1000,  -450,   30,   10,   10,   30,  -450,  1000],
           [  800,  -500,   10,   50,   50,   10,  -500,   800],
           [  800,  -500,   10,   50,   50,   10,  -500,   800],
           [ 1000,  -450,   30,   10,   10,   30,  -450,  1000],
           [-3000, -5000, -450, -500, -500, -450, -5000, -3000],
           [10000, -3000, 1000,  800,  800, 1000, -3000, 10000]]


#################### CLASS PART ####################


class Move :
    """Class representating a move: One tile placed, the rest flipped"""

    def __init__(self, _r :int, _c :int) :
        self.placed = (_r, _c)
        self.flipped :list = []

    def add_to_flipped(self, list_moves) -> None :
        self.flipped.extend(list_moves)


class Board :
    """Class representating the reversi board in memory"""

    def __init__(self):
        # Clear the board and place the 4 initial tiles
        self.b = [[0 for row in range(8)] for col in range(8)]
        self.b[3][3] = -1
        self.b[4][4] = -1
        self.b[3][4] = 1
        self.b[4][3] = 1
        # Human player begins
        self.turn = 1
        # Store the possible legal moves at a turn, initially empty
        self.legal_moves = []
        # Move history of the game, initially empty
        self.moves = []
        # Blinking cursor position and Status
        self.CurX = 0
        self.CurY = 0
        self.CrsrOn = 1
        self.CrsrEn = True

    def is_legal_move(self, mov) -> bool :
        """Check if desired move is legal for the player"""
        return mov in self.legal_moves

    def change_turn(self) -> None :
        """Switch over who's turn it is"""
        self.turn = (-1)*self.turn

    def is_game_over(self) -> bool :
        """Check if game has reached end condition"""
        # Game is over if either the board is full, or none of the players can legally place a tile.
        # Although it doesn't make sense to over-complicate, as if the board is full, then
        # none of the players are able to place one more tile, so it is enough to check
        # for this second condition (is anyone able to move).
        if not len(self.calc_legal_moves(1)) and not len(self.calc_legal_moves(-1)) : return True
        return False

    def calc_legal_moves(self, forWhom :int =0):
        """Calculates legal moves by checking every position
        Parameters:
        :param forWhom : for which Player should it be calculated. Default: Current turn
        :returns : list of legal moves for the requested player"""

        myMoves :list = []
        if not forWhom : forWhom = self.turn
        for i in range(8) :
            for j in range(8) :
                if self.b[i][j] == forWhom :
                    LML = self.check_pos(i, j, forWhom)
                    for z in LML :
                        if z not in myMoves : myMoves.append(z)
        return myMoves

    def check_pos(self, row :int, col :int, plyr :int):
        """Checks whether current pos is at the end of any line
        Parameters:
        :param row : Y position on the board as int
        :param col : X position on the board as int
        :param plyr : for which player are we checking as int
        :returns : list of moves as list"""

        myMoves :list = []
        for Dir in ( (0,1) , (1,1) , (1,0) , (1,-1) , (0,-1) , (-1,-1), (-1,0) , (-1,1) ) :
            row1 = row ; col1 = col ; count = 0
            col1 += Dir[1] ; row1 += Dir[0]
            while col1 < 8 and col1 > -1 and row1 < 8 and row1 > -1 :
                if not self.b[row1][col1] :
                    if count : myMoves.append((row1, col1))
                    break
                if self.b[row1][col1] == plyr :
                    break
                else :
                    count += 1
                col1 += Dir[1] ; row1 += Dir[0]
        return myMoves

    def make_move(self, row :int, col :int, Visualize :bool =False) -> None :
        """Makes move at a certain position
        Parameters :
        :param row : Y position on the board as int
        :param col : X position on the board as int
        :param Visualize : Demonstrate with highlighted pixels on the screen
        :returns : None"""

        current_move = Move(row,col)
        count :list = list(())
        self.b[row][col] = self.turn
        _clr = COLOR["B1"] if self.turn > 0 else COLOR["W1"]
        if Visualize :
            s.set_pixel(col,row,_clr)
            time.sleep(0.3)

        for Dir in ( (0,1) , (1,1) , (1,0) , (1,-1) , (0,-1) , (-1,-1), (-1,0) , (-1,1) ) :
            row1 = row ; col1 = col ; count = []
            col1 += Dir[1] ; row1 += Dir[0]
            while col1 < 8 and col1 > -1 and row1 < 8 and row1 > -1 :
                if not self.b[row1][col1] : break
                if self.b[row1][col1] == self.turn :
                    self.flip_tiles(count)
                    current_move.add_to_flipped(count)
                    if Visualize :
                        for (_rw,_co) in count :
                            s.set_pixel(_co, _rw, _clr)
                            time.sleep(0.3)
                    break
                else :
                    count.append((row1,col1))
                col1 += Dir[1] ; row1 += Dir[0]
        self.moves.append(current_move)

        if Visualize :
            time.sleep(2)
            draw_board()

    def flip_tiles(self, list_moves) -> None :
        """Flip over a tile at certain positions
        Parameters :
        :param list_moves : The coordinate list as a list of iterables
        :returns : None"""
        for pos in list_moves:
            self.b[pos[0]][pos[1]] = (-1)*self.b[pos[0]][pos[1]]

    def undo_move(self) -> None :
        """Technical method, it is able to undo a move based on the history list"""
        mov = self.moves.pop()
        self.b[mov.placed[0]][mov.placed[1]] = 0
        self.flip_tiles(mov.flipped)

    def evaluate_board(self) -> int :
        """Evaluates the board taking into account the weights"""
        score = 0
        for i in range(8):
            for j in range(8):
                if self.b[i][j] == self.turn:
                    score += WEIGHTS[i][j]
                else:
                    score -= WEIGHTS[i][j]
        return +score

    def computer_move(self) -> None :
        """Perform calculations and handle the move at the Computer's turn"""
        global COLOR
        bm = self._get_best_move(0, 4)
        if bm :
            (row, col) = bm
            for l in range(3) :
                s.set_pixel(col,row,COLOR["W1"])
                time.sleep(0.5)
                draw_board()
                time.sleep(0.5)
            self.make_move(row, col, True)
        else :
            s.show_letter('?', text_colour=COLOR["W1"])
            time.sleep(3)
            draw_board()

    def _get_best_move(self, depth, max_depth):
        """Fetches best move from the possibilities
        Parameters :
        :param depth : current level of recursion depth
        :param max_depth : max level of recursion depth
        :returns : the technical score of the step as int"""
        if self.is_game_over() or depth == max_depth : return self.evaluate_board()
        bmov = None
        # As low as possible
        score = -1000000
        for move in self.legal_moves:
            self.make_move(move[0], move[1], False)
            self.change_turn()
            self.legal_moves = self.calc_legal_moves()
            sco = self._get_best_move(depth + 1, max_depth)
            sco = -sco
            if sco > score:
                score = sco
                bmov = move
            self.undo_move()
            self.change_turn()
            self.legal_moves = self.calc_legal_moves()
        if depth == 0:
            return bmov
        else:
            return score


#################### PROC PART ####################


def draw_board() :
    """Refresh the screen according to the actual Board status"""
    global COLOR
    V :list =list(())
    for _rw in range(8):
        for _cl in range(8):
            if reversi.b[_rw][_cl] == -1 :
                V.append(COLOR["W0"])
            elif reversi.b[_rw][_cl] == 1 :
                V.append(COLOR["B0"])
            else :
                V.append([0,0,0])
    s.set_pixels(V)


def clamp(Value :int) -> int :
    """Limit the incoming value to 0..7"""
    return max(min(Value,7),0)

def moveCursor(event) -> None :
    """Handle the stick events"""
    if event.action != "pressed" : return
    if reversi.turn < 1 : return
    if event.direction == "middle" :
        if reversi.is_legal_move((reversi.CurY, reversi.CurX)):
            reversi.CrsrOn = 0
            reversi.CrsrEn = False
            draw_board()
            reversi.make_move(reversi.CurY, reversi.CurX, True)
            reversi.change_turn()
            reversi.legal_moves = reversi.calc_legal_moves()
    else :
        dt = {"up":(0,-1) , "down":(0,1) , "left":(-1,0) , "right":(1,0)}[event.direction]
        reversi.CurX = clamp(reversi.CurX+dt[0]) ; reversi.CurY = clamp(reversi.CurY+dt[1])
        draw_board()



#################### MAIN PART ####################


s = SenseHat()
s.clear()
s.stick.direction_any = moveCursor
reversi = Board()
reversi.legal_moves = reversi.calc_legal_moves(1)
draw_board()

# Main game loop
while not reversi.is_game_over():
    if reversi.turn > 0 :
        reversi.legal_moves = reversi.calc_legal_moves()
        if len(reversi.legal_moves) == 0 :
            s.show_letter('?', text_colour=COLOR["B1"])
            time.sleep(3)
            draw_board()
            reversi.change_turn()
            continue
        reversi.CrsrEn = True
        reversi.CrsrOn = 1-reversi.CrsrOn
        if reversi.CrsrOn :
            s.set_pixel(reversi.CurX, reversi.CurY, [240,240,240])
        else :
            draw_board()
    else :
        reversi.CrsrEn = False
        reversi.CrsrOn = 0
        draw_board()
        reversi.computer_move()
        reversi.change_turn()
        reversi.legal_moves = reversi.calc_legal_moves()
    time.sleep(0.5)

#Announce game results
NumBlack = 0 ; NumWhite = 0
for k in range(8):
    for l in range(8):
        if reversi.b[k][l] == 1 :
            NumBlack += 1
        elif reversi.b[k][l] == -1 :
            NumWhite += 1

if NumBlack > NumWhite :
    _msg = f"Player has won {NumBlack} : {NumWhite}"
elif NumWhite > NumBlack :
    _msg = f"Computer has won {NumWhite} : {NumBlack}"
else :
    _msg = "Draw Game !"

s.show_message(_msg)
s.clear()
