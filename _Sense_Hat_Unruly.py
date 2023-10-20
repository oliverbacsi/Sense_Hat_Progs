
import random

class Game :
    """Stores general game parameters"""

    def __init__(self) :
        self.grid :list = list(())
        self.errors :list = list(())
        self.immutable :list = list(())
        self.completed :bool =False
        for i in range(64) :
            self.grid.append(0)
            self.errors.append(0)
            self.immutable.append(False)
        self.ones_rows  :list = [0,0,0,0,0,0,0,0]
        self.ones_cols  :list = [0,0,0,0,0,0,0,0]
        self.zeros_rows :list = [0,0,0,0,0,0,0,0]
        self.zeros_cols :list = [0,0,0,0,0,0,0,0]

    def update_counts(self) -> None :
        """Update the ones_rows..zeros_cols vectors based on the current grid status"""
        self.ones_rows  = [0,0,0,0,0,0,0,0]
        self.ones_cols  = [0,0,0,0,0,0,0,0]
        self.zeros_rows = [0,0,0,0,0,0,0,0]
        self.zeros_cols = [0,0,0,0,0,0,0,0]
        for j in range(8) :
            for i in range(8) :
                if self.grid[8*j+i] == 1 :
                    self.ones_rows[j] += 1
                    self.ones_cols[i] += 1
                elif self.grid[8*j+i] == 2 :
                    self.zeros_rows[j] += 1
                    self.zeros_cols[i] += 1

    def solve(self) -> None :
        """The main Solve algo that calls all others.
        Maiden name: unruly_solve_game"""
        while True :
            # Keep repeating checks from easiest to the hardest as long as they produce outputs

            # Check for impending 3's
            if self.unruly_solver_check_all_threes() : continue
            # Check for rows with only one unfilled square
            if self.unruly_solver_check_all_one_color_complete() : continue
            # Check for impending failures of row/column uniqueness, if it's enabled in this game mode
            if self.unruly_solver_check_all_uniques() : continue
            # Check for nearly completed rows
            if self.unruly_solver_check_all_near_complete() : continue

            # If we have reached this pont so far with no improvement, then exit.
            break

    def unruly_solver_check_all_threes(self) -> int :
        ret :int =0
        ret += self.unruly_solver_check_threes(True, 1, 2)
        ret += self.unruly_solver_check_threes(True, 2, 1)
        ret += self.unruly_solver_check_threes(False,1, 2)
        ret += self.unruly_solver_check_threes(False,2, 1)
        return ret

    def unruly_solver_check_threes(self, horizontal :bool, check :int, block :int) -> int :
        """Check for any three squares which almost form three in a row"""
        dx :int = 1 if horizontal else 0
        dy :int = 1-dx
        sx :int = dx ; sy :int = dy
        ex :int = 8-dx ; ey :int = 8-dy
        ret :int = 0

        for y in range(sy, ey) :
            for x in range(sx, ex) :
                i1 = (y-dy) *8 + (x-dx)
                i2 = y*8 + x
                i3 = (y+dy) *8 + (x+dx)
                if (self.grid[i1], self.grid[i2], self.grid[i3]) == (check,check,0) :
                    ret+=1
                    self.grid[i3] = block
                if (self.grid[i1], self.grid[i2], self.grid[i3]) == (check,0,check) :
                    ret+=1
                    self.grid[i2] = block
                if (self.grid[i1], self.grid[i2], self.grid[i3]) == (0,check,check) :
                    ret+=1
                    self.grid[i1] = block
        self.update_counts()
        return ret

    def unruly_solver_check_all_one_color_complete(self) -> int :
        ret :int =0
        ret += self.unruly_solver_check_one_color_complete(True,  2)
        ret += self.unruly_solver_check_one_color_complete(False, 2)
        ret += self.unruly_solver_check_one_color_complete(True,  1)
        ret += self.unruly_solver_check_one_color_complete(False, 1)
        return ret

    def unruly_solver_check_one_color_complete(self, horizontal :bool, fill :int) -> int :
        """Check for completed rows/cols for one number, then fill in the rest"""
        ret :int =0
        self.update_counts()
        if horizontal :
            if fill == 2 :
                for i in range(8) :
                    if self.ones_rows[i] == 4 and self.zeros_rows[i] < 4 :
                        ret += self.unruly_solver_fill_row(i, horizontal, fill)
            elif fill == 1 :
                for i in range(8) :
                    if self.zeros_rows[i] == 4 and self.ones_rows[i] < 4 :
                        ret += self.unruly_solver_fill_row(i, horizontal, fill)
        else :
            if fill == 2 :
                for i in range(8) :
                    if self.ones_cols[i] == 4 and self.zeros_cols[i] < 4 :
                        ret += self.unruly_solver_fill_row(i, horizontal, fill)
            elif fill == 1 :
                for i in range(8) :
                    if self.zeros_cols[i] == 4 and self.ones_cols[i] < 4 :
                        ret += self.unruly_solver_fill_row(i, horizontal, fill)
        return ret

    def unruly_solver_fill_row(self, i :int, horizontal :bool, fill :int) -> int :
        """Place a number in every empty square in a row/column"""
        ret :int =0
        for j in range(8) :
            p = i*8+j if horizontal else j*8+i
            if self.grid[p] == 0 :
                ret+=1
                self.grid[p] = fill
        self.update_counts()
        return ret

    def unruly_solver_check_all_uniques(self) -> int :
        ret :int =0
        ret += self.unruly_solver_check_uniques(True,  1, 2)
        ret += self.unruly_solver_check_uniques(True,  2, 1)
        ret += self.unruly_solver_check_uniques(False, 1, 2)
        ret += self.unruly_solver_check_uniques(False, 2, 1)
        return ret

    def unruly_solver_check_uniques(self, horizontal: bool, check :int, block :int) -> int :
        """Find each row that has max entries of type 'check', and see if all those entries match those
        in any row with max-1 entries. If so, set the last non-matching entry of the latter row to ensure
        that it's different."""
        rmult :int = 8 if horizontal else 1
        cmult :int = 1 if horizontal else 8
        ret :int =0

        for r in range(8) :
            if rowcount[r] != 4 : continue
            for r2 in range(8) :
                nmatch = 0 ; nonmatch = -1
                if rowcount[r2] != 3 : continue
                for c in range(8) :
                    if g.grid[r*rmult + c*cmult] == check :
                        if g.grid[r2*rmult + c*cmult] == check :
                            nmatch+=1
                        else :
                            nonmatch = c
                if nmatch == 3 :
                    i1 = r2 * rmult + nonmatch * cmult
                    # assert(nonmatch != -1);  -- Raise exception ???
                    if g.grid[i1] == block : continue
                    # assert(state->grid[i1] == EMPTY);
                    g.grid[i1] = block
                    if block == 1 :
                        scratch.ones_rows[i1 / 8]+=1
                        scratch.ones_cols[i1 % 8]+=1
                    else :
                        scratch.zeros_rows[i1 / 8]+=1
                        scratch.zeros_cols[i1 % 8]+=1
                    ret+=1
        return ret










def unruly_solver_check_near_complete(complete :int, horizontal :bool, rowcount :int, colcount :int, fill: int) -> int :
    """This function checks for a row with one Y remaining, then looks for positions that could cause
    the remaining squares in the row to make 3 X's in a row. Example:
    Consider the following row:  1 1 0 . . .
    If the last 1 was placed in the last square, the remaining squares would be 0:  1 1 0 0 0 1
    This violates the 3 in a row rule. We now know that the last 1 shouldn't be in the last cell:  1 1 0 . . 0
    """
    ###+++TODO: w2,h2=8 ; w,h=4 ; törölhető ha oké
    dx :int = 1 if horizontal else 0 ; dy :int = 1-dx
    sx :int =dx ; sy :int =dy
    ex :int =8-dx ; ey :int = 8-dy
    ret :int =0

    # Check for any two blank and one filled square
    for y in range(sy,ey) :
        # One type must have 1 remaining, the other at least 2
        if horizontal and (complete[y] < 3 or rowcount[y] > 2) : continue
        for x in range(sx,ex) :
            if not horizontal and (complete[x] < 3 or colcount[x] > 2) : continue
            i = y if horizontal else x
            i1 = (y-dy)*8 + (x-dx)
            i2 = y*8 + x
            i3 = (y+dy)*8 + (x+dx)
            if g.grid[i1] == fill and g.grid[i2] == 0 and g.grid[i3] == 0 :
                # Temporarily fill the empty spaces with something else. This avoids raising the counts for the row and column
                g.grid[i2] =3 ; g.grid[i3] =3
                ret += unruly_solver_fill_row(i, horizontal, rowcount, colcount, fill)
                g.grid[i2] =0 ; g.grid[i3] =0
            elif g.grid[i1] == 0 and g.grid[i2] == fill and g.grid[i3] == 0 :
                g.grid[i1] =3 ; g.grid[i3] =3
                ret += unruly_solver_fill_row(i, horizontal, rowcount, colcount, fill)
                g.grid[i1] =0 ; g.grid[i3] =0
            elif g.grid[i1] == 0 and g.grid[i2] == 0 and g.grid[i3] == fill :
                g.grid[i1] =3 ; g.grid[i2] =3
                ret += unruly_solver_fill_row(i, horizontal, rowcount, colcount, fill)
                g.grid[i1] =0 ; g.grid[i2] =0
            elif g.grid[i1] == 0 and g.grid[i2] == 0 and g.grid[i3] == 0 :
                g.grid[i1] =3 ; g.grid[i2] =3 ; g.grid[i3] =3
                ret += unruly_solver_fill_row(i, horizontal, rowcount, colcount, fill)
                g.grid[i1] =0 ; g.grid[i2] =0 ; g.grid[i3] =0
    return ret

def unruly_solver_check_all_near_complete(scratch) -> int :
    ret: int = 0
    ret += unruly_solver_check_near_complete(scratch.ones_rows,  True,  scratch.zeros_rows, scratch.zeros_cols, 2)
    ret += unruly_solver_check_near_complete(scratch.ones_cols,  False, scratch.zeros_rows, scratch.zeros_cols, 2)
    ret += unruly_solver_check_near_complete(scratch.zeros_rows, True,  scratch.ones_rows,  scratch.ones_cols,  1)
    ret += unruly_solver_check_near_complete(scratch.zeros_cols, False, scratch.ones_rows,  scratch.ones_cols,  1)
    return ret



def unruly_validate_rows(gms3, horizontal :bool, check :int) -> int :
    """Check for any three in a row, and mark errors accordingly (if required)"""
    dx :int = 1 if horizontal else 0 ; dy :int = 1-dx
    sx :int =dx ; sy :int =dy
    ex :int =8-dx ; ey :int =8-dy
    ret: int = 0

    err1 :int = 1 if horizontal else 4
    err2 :int = 3 if horizontal else 12
    err3 :int = 2 if horizontal else 8

    for y in range(sy,ey) :
        for x in range(sx,ex) :
            i1 = (y-dy)*8 + (x-dx)
            i2 = y*8 + x
            i3 = (y+dy)*8 + (x+dx)
            if gms3.grid[i1] == check and gms3.grid[i2] == check and gms3.grid[i3] == check :
                ret+=1
                gms3.errors[i1] |= err1
                gms3.errors[i2] |= err2
                gms3.errors[i3] |= err3
    return ret

def unruly_validate_unique(gms4, horizontal :bool) -> int :
    """Check for any two full rows matching exactly, and mark errors accordingly (if required)"""
    rmult :int = 8 if horizontal else 1
    cmult :int = 1 if horizontal else 8
    ###+++TODO: nr,nc=8 , lehet törölni ha oké
    err :int = 32 if horizontal else 64
    ret: int = 0

    for r in range(8) :
        nfull = 0
        for c in range(8) :
            if gms4.grid[r*rmult + c*cmult] != 0 : nfull+=1
        if nfull != 8 : continue
        for r2 in range(r+1,8) :
            match = True
            for c in range(8) :
                if gms4.grid[r*rmult + c*cmult] != gms4.grid[r2*rmult + c*cmult] : match =False
            if match :
                for c in range(8) :
                gms4.errors[r*rmult + c*cmult] |= err
                gms4.errors[r2*rmult + c*cmult] |= err
                ret+=1
    return ret

def unruly_validate_all_rows(gms2) -> int :
    errcount :int =0
    errcount += unruly_validate_rows(gms2,True,  1)
    errcount += unruly_validate_rows(gms2,False, 1)
    errcount += unruly_validate_rows(gms2,True,  2)
    errcount += unruly_validate_rows(gms2,False, 2)
    errcount += unruly_validate_unique(gms2, True)
    errcount += unruly_validate_unique(gms2, False)
    return -1 if errcount else 0

def unruly_validate_counts(scr1) -> int :
    """See if all rows/columns are satisfied. If one is exceeded, mark it as an error (if required)"""
    below :bool =False ; above :bool =False

    for i in range(8) :
        if scr1.ones_cols[i]  < 4 : below =True
        if scr1.zeros_cols[i] < 4 : below =True
        if scr1.ones_cols[i]  > 4 : above =True
        if scr1.zeros_cols[i] > 4 : above =True
    for i in range(8) :
        if scr1.ones_rows[i]  < 4 : below =True
        if scr1.zeros_rows[i] < 4 : below =True
        if scr1.ones_rows[i]  > 4 : above =True
        if scr1.zeros_rows[i] > 4 : above =True

    if above : return -1
    if below : return 1
    return 0






# this is not called directly, its name is forwarded to the main game struct of sgt_puzzles
#def solve_game(gms, curst) -> str :
#
#    ret :str =""
#    solved = gms
#    sc1 = Scratch()
#
#    unruly_solve_game(solved, sc1, 3)
#    result :int = unruly_validate_counts(sc1)
#    if unruly_validate_all_rows(solved, []) == -1 : result = -1
#    if result == 0 :
#        ret = "S"
#        for i in range(64) : ret+= "1" if solved.grid[i] == 1 else "0"
#    return ret



### GENERATOR ###



def unruly_fill_game(gms, scr) -> bool :
    """Construct a valid filled grid by repeatedly picking an unfilled space and fill it,
    then calling the solver to fill in any spaces forced by the change.
    """

    # Generate random array of spaces
    s1 = list(range(64))
    spaces :list =list(())
    for i in range(64) : spaces.append(s1.pop(random.randint(0,len(s1)-1)))
    for j in range(64) :
        i = spaces[j]
        if gms.grid[i] != 0 : continue
        if random.randint(0,1) :
            gms.grid[i] = 1
            scr.ones_rows[i/8]+=1
            scr.ones_cols[i%8]+=1
        else :
            gms.grid[i] = 2
            scr.zeros_rows[i/8]+=1
            scr.zeros_cols[i%8]+=1
        unruly_solve_game(gms, scr, 3)

    if unruly_validate_all_rows(gms) != 0 or unruly_validate_counts(scr) != 0 : return False
    return True


def new_game_desc(rs, aux :str, interactive :bool) -> None :
    global gs, sc
    spaces :list =list(())

    while True :

        while True :
            gs = Game()
            sc = Scratch()
            if unruly_fill_game(gs,sc) : break

        # Generate random array of spaces
        s1 = list(range(64))
        for i in range(64) : spaces.append(s1.pop(random.randint(0, len(s1) - 1)))
        # Winnow the clues by starting from our filled grid, repeatedly picking a filled space and emptying it,
        # as long as the solver reports that the puzzle can still be solved after doing so.
        for j in range(64) :
            i = spaces[j]
            c = gs.grid[i]
            gs.grid[i] =0

            solver = gs
            scrx = Scratch()
            unruly_solve_game(solver, scrx, 2)
            if unruly_validate_counts(scrx) != 0 : gs.grid[i] =c

        # See if the game has accidentally come out too easy.
        solver = gs
        scrx = Scratch()
        unruly_solve_game(solver, scrx, 1)
        if unruly_validate_counts(scrx) > 0 : break


gs = Game()
sc = Scratch()
