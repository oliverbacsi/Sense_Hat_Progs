#!/usr/bin/env python3
###########################################
# The classic Reversi game for Sense Hat


#################### INIT PART ####################

import sys,random,time
import sense_hat

COLOR :dict = {"W1":[255,0,0], "W0":[160,0,0], "B1":[0,0,255], "B0":[0,0,160]}

# Advanced weightage
WEIGHTS = [[10000, -3000, 1000,  800,  800, 1000, -3000, 10000],
           [-3000, -5000, -450, -500, -500, -450, -5000, -3000],
           [ 1000,  -450,   30,   10,   10,   30,  -450,  1000],
           [  800,  -500,   10,   50,   50,   10,  -500,   800],
           [  800,  -500,   10,   50,   50,   10,  -500,   800],
           [ 1000,  -450,   30,   10,   10,   30,  -450,  1000],
           [-3000, -5000, -450, -500, -500, -450, -5000, -3000],
           [10000, -3000, 1000,  800,  800, 1000, -3000, 10000]]

def other(color :int):
    return (-1)*color


#################### CLASS PART ####################


class Move():
    """
    Class representating a move: One token placed, the rest flipped
    """
    def __init__(self, _r :int, _c :int) :
        self.placed = (_r, _c)
        self.flipped = []

    def add_to_flipped(self, list_moves):
        self.flipped.extend(list_moves)


class Board():
    """
    Class representating the reversi board in memory
    """
    def __init__(self):
        self.b = [[0 for row in range(8)] for col in range(8)]
        self.b[3][3] = -1
        self.b[4][4] = -1
        self.b[3][4] = 1
        self.b[4][3] = 1
        self.turn = 1
        self.legal_moves = []
        self.winner = None
        self.moves = []
        self.CurX = 0
        self.CurY = 0
        self.CrsrOn = 1
        self.CrsrEn = True

    def is_legal_move(self, mov) -> bool :
        return mov in self.legal_moves

    def change_turn(self) -> None :
        self.turn = (-1)*self.turn

    def is_game_over(self) -> bool :
        if not len(self.calc_legal_moves(1)) and not len(self.calc_legal_moves(-1)) : return True
        return False

    def calc_legal_moves(self, forWhom :int =0):
        """
        Calculates legal moves by checking every position
        Parameters:
        forWhom : for which Player should it be calculated. Default: Current turn
        Returns: list of legal moves for the requested player
        """
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
        """
        Checks whether current pos is at the end of any line
        """
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

    def make_move(self, row :int, col :int, Visualize :bool =False):
        """
        Makes move at a certain position
        """
        current_move = Move(row,col)
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
                    self.flip_tokens(count)
                    current_move.add_to_flipped(count)
                    if Visualize :
                        for (_rw,_co) in count :
                            s.set_pixel(_rw, _co, _clr)
                            time.sleep(0.3)
                    break
                else :
                    count.append((row1,col1))
                col1 += Dir[1] ; row1 += Dir[0]

        if Visualize :
            time.sleep(2)
            draw_board()

    def flip_tokens(self, list_moves):
        for pos in list_moves:
            self.b[pos[0]][pos[1]] = (-1)*self.b[pos[0]][pos[1]]

    def undo_move(self):
        mov = self.moves.pop()
        self.b[mov.placed[0]][mov.placed[1]] = 0
        self.flip_tokens(mov.flipped)

    def evaluate_board(self):
        """
        Evaluates the board taking into account the weights
        """
        score = 0
        for i in range(8):
            for j in range(8):
                if self.b[i][j] == self.turn:
                    score += WEIGHTS[i][j]
                else:
                    score -= WEIGHTS[i][j]
        return +score

    def computer_move(self):
        (row, col) = self._get_best_move(0, 4)
        self.make_move(row, col, True)

    def _get_best_move(self, depth, max_depth):
        """
        Fetches best move
        """
        if self.is_game_over() or depth == max_depth:
            # print("depth == " + str(max_depth) + " Player = " + self.turn + " Score = " + str(self.evaluate_board()))
            return self.evaluate_board()
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
    """
    Refresh the screen according to the actual Board status
    """
    global COLOR
    V :list =list(())
    for i in range(8):
        for j in range(8):
            if reversi.b[i][j] == -1 :
                V.append(COLOR["W0"])
            elif reversi.b[i][j] == 1 :
                V.append(COLOR["B0"])
            else :
                V.append([0,0,0])
    s.set_pixels(V)


def crsr_U(event) :
    if reversi.turn < 1 : return
    if event.action == "pressed" :
        if reversi.CurY > 0 : reversi.CurY -= 1
        draw_board()

def crsr_D(event) :
    if reversi.turn < 1 : return
    if event.action == "pressed" :
        if reversi.CurY < 7 : reversi.CurY += 1
        draw_board()

def crsr_L(event) :
    if reversi.turn < 1 : return
    if event.action == "pressed" :
        if reversi.CurX > 0 : reversi.CurX -= 1
        draw_board()

def crsr_R(event) :
    if reversi.turn < 1 : return
    if event.action == "pressed" :
        if reversi.CurX < 7 : reversi.CurX += 1
        draw_board()

def tryUserStep(event) :
    if reversi.turn < 1 : return
    if event.action == "pressed" :
        print(f"\n{reversi.CurY} , {reversi.CurX}")
        print(str(reversi.legal_moves))
        if reversi.is_legal_move((reversi.CurY, reversi.CurX)):
            reversi.CrsrOn = 0
            reversi.CrsrEn = False
            draw_board()
            reversi.make_move(reversi.CurY, reversi.CurX, True)
            reversi.change_turn()
            reversi.legal_moves = reversi.calc_legal_moves()


#################### MAIN PART ####################


s = sense_hat.SenseHat()
s.clear()
s.stick.direction_up = crsr_U
s.stick.direction_down = crsr_D
s.stick.direction_left = crsr_L
s.stick.direction_right = crsr_R
s.stick.direction_middle = tryUserStep


reversi = Board()
draw_board()

while not reversi.is_game_over():
    if reversi.turn > 0 :
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
        reversi.legal_modes = reversi.calc_legal_moves()
    time.sleep(0.5)

#Announce game results
NumBlack = 0 ; NumWhite = 0
for i in range(8):
    for j in range(8):
        if reversi.b[i][j] == 1 :
            NumBlack += 1
        elif reversi.b[i][j] == -1 :
            NumWhite += 1

if NumBlack > NumWhite :
    _msg = f"Blue has won {NumBlack} : {NumWhite}"
elif NumWhite > NumBlack :
    _msg = f"Red has won {NumWhite} : {NumBlack}"
else :
    _msg = "Draw Game !"

s.show_message(_msg)
s.clear()
