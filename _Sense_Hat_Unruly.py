#!/usr/bin/env python3
##########################################
# Unruly Game
#

#################### INIT PART ####################

import random, time
import sense_hat

#################### CLASS PART ####################

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
        self.update_counts()
        if horizontal :
            if check == 1 :
                for i in range(8) :
                    if self.ones_rows[i] != 4 : continue
                    for r2 in range(8) :
                        nmatch = 0 ; nonmatch = -1
                        if self.ones_rows[r2] != 3 : continue
                        for c in range(8) :
                            if self.grid[i*rmult + c*cmult] == check :
                                if self.grid[r2*rmult + c*cmult] == check :
                                    nmatch+=1
                                else :
                                    nonmatch = c
                        if nmatch == 3 :
                            i1 = r2 * rmult + nonmatch * cmult
                            self.grid[i1] = block
                            self.update_counts()
                            ret+=1
            elif check == 2 :
                for i in range(8) :
                    if self.zeros_rows[i] != 4 : continue
                    for r2 in range(8) :
                        nmatch = 0 ; nonmatch = -1
                        if self.zeros_rows[r2] != 3 : continue
                        for c in range(8) :
                            if self.grid[i*rmult + c*cmult] == check :
                                if self.grid[r2*rmult + c*cmult] == check :
                                    nmatch+=1
                                else :
                                    nonmatch = c
                        if nmatch == 3 :
                            i1 = r2 * rmult + nonmatch * cmult
                            self.grid[i1] = block
                            self.update_counts()
                            ret+=1
        else :
            if check == 1 :
                for i in range(8) :
                    if self.ones_cols[i] != 4 : continue
                    for r2 in range(8) :
                        nmatch = 0 ; nonmatch = -1
                        if self.ones_cols[r2] != 3 : continue
                        for c in range(8) :
                            if self.grid[i*rmult + c*cmult] == check :
                                if self.grid[r2*rmult + c*cmult] == check :
                                    nmatch+=1
                                else :
                                    nonmatch = c
                        if nmatch == 3 :
                            i1 = r2 * rmult + nonmatch * cmult
                            self.grid[i1] = block
                            self.update_counts()
                            ret+=1
            elif check == 2 :
                for i in range(8) :
                    if self.zeros_cols[i] != 4 : continue
                    for r2 in range(8) :
                        nmatch = 0 ; nonmatch = -1
                        if self.zeros_cols[r2] != 3 : continue
                        for c in range(8) :
                            if self.grid[i*rmult + c*cmult] == check :
                                if self.grid[r2*rmult + c*cmult] == check :
                                    nmatch+=1
                                else :
                                    nonmatch = c
                        if nmatch == 3 :
                            i1 = r2 * rmult + nonmatch * cmult
                            self.grid[i1] = block
                            self.update_counts()
                            ret+=1
        return ret

    def unruly_solver_check_all_near_complete(self) -> int :
        ret: int = 0
        #ret += self.unruly_solver_check_near_complete(scratch.ones_rows,  True,  scratch.zeros_rows, scratch.zeros_cols, 2)
        #ret += self.unruly_solver_check_near_complete(scratch.zeros_rows, True,  scratch.ones_rows,  scratch.ones_cols,  1)
        #ret += self.unruly_solver_check_near_complete(scratch.ones_cols,  False, scratch.zeros_rows, scratch.zeros_cols, 2)
        #ret += self.unruly_solver_check_near_complete(scratch.zeros_cols, False, scratch.ones_rows,  scratch.ones_cols,  1)
        #def unruly_solver_check_near_complete(complete :int, horizontal :bool, rowcount :int, colcount :int, fill: int)
        ret += self.unruly_solver_check_near_complete(True,  2)
        ret += self.unruly_solver_check_near_complete(False, 2)
        ret += self.unruly_solver_check_near_complete(True,  1)
        ret += self.unruly_solver_check_near_complete(False, 1)
        return ret

    def unruly_solver_check_near_complete(self, horizontal :bool, fill: int) -> int :
        """This function checks for a row with one Y remaining, then looks for positions that could cause
        the remaining squares in the row to make 3 X's in a row. Example:
        Consider the following row:  1 1 0 . . .
        If the last 1 was placed in the last square, the remaining squares would be 0:  1 1 0 0 0 1
        This violates the 3 in a row rule. We now know that the last 1 shouldn't be in the last cell:  1 1 0 . . 0
        """
        dx :int = 1 if horizontal else 0 ; dy :int = 1-dx
        sx :int =dx ; sy :int =dy
        ex :int =8-dx ; ey :int = 8-dy
        ret :int =0

        if horizontal :
            if fill == 2 :
                # Check for any two blank and one filled square
                for y in range(sy,ey) :
                    # One type must have 1 remaining, the other at least 2
                    if self.ones_rows[y] < 3 or self.zeros_rows[y] > 2 : continue
                    for x in range(sx,ex) :
                        i1 = y*8 + (x-1)
                        i2 = y*8 + x
                        i3 = y*8 + (x+1)
                        gm = (self.grid[i1], self.grid[i2], self.grid[i3])
                        if gm in ( (2,0,0) , (0,2,0) , (0,0,2) , (0,0,0) ) :
                            for coi in (i1,i2,i3) :
                                if self.grid[coi] == 0 : self.grid[coi] = 3
                            ret += self.unruly_solver_fill_row(y, True, 2)
                            for coi in (i1,i2,i3) :
                                if self.grid[coi] == 3 : self.grid[coi] = 0
            elif fill == 1 :
                # Check for any two blank and one filled square
                for y in range(sy,ey) :
                    # One type must have 1 remaining, the other at least 2
                    if self.zeros_rows[y] < 3 or self.ones_rows[y] > 2 : continue
                    for x in range(sx,ex) :
                        i1 = y*8 + (x-1)
                        i2 = y*8 + x
                        i3 = y*8 + (x+1)
                        gm = (self.grid[i1], self.grid[i2], self.grid[i3])
                        if gm in ( (1,0,0) , (0,1,0) , (0,0,1) , (0,0,0) ) :
                            for coi in (i1,i2,i3) :
                                if self.grid[coi] == 0 : self.grid[coi] = 3
                            ret += self.unruly_solver_fill_row(y, True, 1)
                            for coi in (i1,i2,i3) :
                                if self.grid[coi] == 3 : self.grid[coi] = 0
        else :
            if fill == 2 :
                # Check for any two blank and one filled square
                for y in range(sy,ey) :
                    # One type must have 1 remaining, the other at least 2
                    for x in range(sx,ex) :
                        if self.ones_cols[x] < 3 or self.zeros_cols[x] > 2 : continue
                        i1 = (y-1)*8 + x
                        i2 = y*8 + x
                        i3 = (y+1)*8 + x
                        gm = (self.grid[i1], self.grid[i2], self.grid[i3])
                        if gm in ( (2,0,0) , (0,2,0) , (0,0,2) , (0,0,0) ) :
                            for coi in (i1,i2,i3) :
                                if self.grid[coi] == 0 : self.grid[coi] = 3
                            ret += self.unruly_solver_fill_row(x, False, 2)
                            for coi in (i1,i2,i3) :
                                if self.grid[coi] == 3 : self.grid[coi] = 0
            elif fill == 1 :
                # Check for any two blank and one filled square
                for y in range(sy,ey) :
                    # One type must have 1 remaining, the other at least 2
                    for x in range(sx,ex) :
                        if self.zeros_cols[x] < 3 or self.ones_cols[x] > 2 : continue
                        i1 = (y-1)*8 + x
                        i2 = y*8 + x
                        i3 = (y+1)*8 + x
                        gm = (self.grid[i1], self.grid[i2], self.grid[i3])
                        if gm in ( (1,0,0) , (0,1,0) , (0,0,1) , (0,0,0) ) :
                            for coi in (i1,i2,i3) :
                                if self.grid[coi] == 0 : self.grid[coi] = 3
                            ret += self.unruly_solver_fill_row(x, False, 1)
                            for coi in (i1,i2,i3) :
                                if self.grid[coi] == 3 : self.grid[coi] = 0
        return ret

    def validate_all_rows(self) -> int :
        errcount :int =0
        errcount += self.validate_rows(True,  1)
        errcount += self.validate_rows(False, 1)
        errcount += self.validate_rows(True,  2)
        errcount += self.validate_rows(False, 2)
        errcount += self.validate_unique(True)
        errcount += self.validate_unique(False)
        return -1 if errcount else 0

    def validate_rows(self, horizontal :bool, check :int) -> int :
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
                if (self.grid[i1], self.grid[i2], self.grid[i3]) == (check, check, check) :
                    ret+=1
                    self.errors[i1] |= err1
                    self.errors[i2] |= err2
                    self.errors[i3] |= err3
        return ret

    def validate_counts(self) -> int :
        """See if all rows/columns are satisfied. If one is exceeded, mark it as an error (if required)"""
        ret :int =0

        for i in range(8) :
            if self.ones_cols[i]  != 4 : ret+=1
            if self.zeros_cols[i] != 4 : ret+=1
        for i in range(8) :
            if self.ones_rows[i]  != 4 : ret+=1
            if self.zeros_rows[i] != 4 : ret+=1
        return ret

    def validate_unique(self, horizontal :bool) -> int :
        """Check for any two full rows matching exactly, and mark errors accordingly (if required)"""
        rmult :int = 8 if horizontal else 1
        cmult :int = 1 if horizontal else 8
        err :int = 32 if horizontal else 64
        ret :int = 0

        for r in range(8) :
            nfull = 0
            for c in range(8) :
                if self.grid[r*rmult + c*cmult] != 0 : nfull+=1
            if nfull != 8 : continue
            for r2 in range(r+1,8) :
                match = True
                for c in range(8) :
                    if self.grid[r*rmult + c*cmult] != self.grid[r2*rmult + c*cmult] : match =False
                if match :
                    for c in range(8) :
                        self.errors[r*rmult + c*cmult] |= err
                        self.errors[r2*rmult + c*cmult] |= err
                        ret+=1
        return ret


    def generator_fill_game(self) -> bool :
        """Construct a valid filled grid by repeatedly picking an unfilled space and fill it,
       then calling the solver to fill in any spaces forced by the change.
       """

        # Generate random array of spaces
        s1 = list(range(64))
        spaces :list =list(())
        for i in range(64) : spaces.append(s1.pop(random.randint(0,len(s1)-1)))
        for j in range(64) :
            i = spaces[j]
            if self.grid[i] != 0 : continue
            if random.randint(0,1) :
                self.grid[i] = 1
                self.ones_rows[i/8]+=1
                self.ones_cols[i%8]+=1
            else :
                self.grid[i] = 2
                self.zeros_rows[i/8]+=1
                self.zeros_cols[i%8]+=1
            self.solve()

        if self.validate_all_rows() != 0 or self.validate_counts() != 0 : return False
        return True



#################### PROC PART ####################



#################### MAIN PART ####################


spc :list =list(())

while True :

    while True :
        g = Game()
        if g.generator_fill_game() : break

        # Generate random array of spaces
        s2 = list(range(64))
        for i8 in range(64) : spc.append(s2.pop(random.randint(0, len(s2) - 1)))
        # Winnow the clues by starting from our filled grid, repeatedly picking a filled space and emptying it,
        # as long as the solver reports that the puzzle can still be solved after doing so.
        for j8 in range(64) :
            i8 = spc[j8]
            c8 = g.grid[i8]
            g.grid[i8] =0

            solver = g
            solver.solve()
            if solver.validate_counts() != 0 : g.grid[i8] =c8

        # See if the game has accidentally come out too easy.
        #solver = gs
        #scrx = Scratch()
        #unruly_solve_game(solver, scrx, 1)
        if solver.validate_counts() > 0 : break
