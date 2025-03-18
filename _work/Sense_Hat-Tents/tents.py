
TableElement :dict = {"BLANK":0, "TREE":1, "TENT":2, "NONTENT":3, "MAGIC":4}

class Game_Params :
    def __init__(self) :
        self.w :int = -1
        self.h :int = -1
        self.diff :int = -1

    def default_params(self) :
        self.w = 8
        self.h = 8
        self.diff = 1


class Numbers :
    def __init__(self) :
        self.refcount :int =-1
        self.numbers :list =[]

class Game_State :
    def __init__(self) :
        self.p =None
        self.grid :str =""
        self.numbers =None
        self.completed :bool =False
        self.used_solve :bool =False

dx :list = [0,0,-1,1,0,0,0]
dy :list = [0,-1,0,0,1,0,0]
F  :list = [5,4,3,2,1,0]

class Solver_Scratch :
    def __init__(self) :
        self.links :list =[]
        self.locs :list =[]
        self.place :str =""
        self.mrows :str =""
        self.trows :str =""

    def new_scratch(w :int, h :int) -> None:
        self.links = [None] *w*h
        self.locs = [0] * max(w,h)
        self.pace = " " * max(w,h)
        self.mrows = " " * 3*max(w,h)
        self.trows = " " * 3*max(w,h)


def tents_solve(w :int, h :int, grid :list, numbers :list, soln :list, sc, diff :int) -> int :
    global Table_Element, dx, dy
    x :int
    y :int
    d :int
    i :int
    j :int
    mrow :str
    trow :str
    trow1 :str
    trow2 :str
    linkd :int

    sc.links = [None] *w*h
    soln = grid[0:w*h]

    # Main solver loop.
    done_something :bool =False
    while True :

        # Any tent which has only one unattached tree adjacent to it can be tied to that tree.
        for y in range(h) :
            for x in range(w) :
                if soln[y*w+x] == Table_Element["TENT"] and not sc.links[y*w+x] :
                    linkd = 0
                    d = 1
                    while d < 5 :
                        x2 = x + dx[d]
                        y2 = y + dy[d]
                        if x2 in range(w) and y2 in range(h) and soln[y2*w+x2] == Table_Element["TREE"] and not sc.links[y2*w+x2] :
                            if linkd :
                                break
                            else :
                                linkd = d
                        d += 1
                    if d == 5 and linkd == 0 :
                        return 0 ; # No solution exists
                    elif d == 5 :
                        x2 = x + dx[linkd]
                        y2 = y + dy[linkd]
                        sc.links[y*w+x]   =   linkd
                        sc.links[y2*w+x2] = F[linkd]
                        done_something = True

        if done_something : continue
        if diff < 0 : break

###%%%+++ INNEN FOLYT, 8 space szintről



	/*
	 * Mark a blank square as NONTENT if it is not orthogonally
	 * adjacent to any unmatched tree.
	 */
	for (y = 0; y < h; y++)
	    for (x = 0; x < w; x++)
		if (soln[y*w+x] == BLANK) {
		    bool can_be_tent = false;

		    for (d = 1; d < MAXDIR; d++) {
			int x2 = x + dx(d), y2 = y + dy(d);
			if (x2 >= 0 && x2 < w && y2 >= 0 && y2 < h &&
			    soln[y2*w+x2] == TREE &&
			    !sc->links[y2*w+x2])
			    can_be_tent = true;
		    }

		    if (!can_be_tent) {
#ifdef SOLVER_DIAGNOSTICS
			if (verbose)
			    printf("%d,%d cannot be a tent (no adjacent"
				   " unmatched tree)\n", x, y);
#endif
			soln[y*w+x] = NONTENT;
			done_something = true;
		    }
		}

	if (done_something)
	    continue;

	/*
	 * Mark a blank square as NONTENT if it is (perhaps
	 * diagonally) adjacent to any other tent.
	 */
	for (y = 0; y < h; y++)
	    for (x = 0; x < w; x++)
		if (soln[y*w+x] == BLANK) {
		    int dx, dy;
                    bool imposs = false;

		    for (dy = -1; dy <= +1; dy++)
			for (dx = -1; dx <= +1; dx++)
			    if (dy || dx) {
				int x2 = x + dx, y2 = y + dy;
				if (x2 >= 0 && x2 < w && y2 >= 0 && y2 < h &&
				    soln[y2*w+x2] == TENT)
				    imposs = true;
			    }

		    if (imposs) {
#ifdef SOLVER_DIAGNOSTICS
			if (verbose)
			    printf("%d,%d cannot be a tent (adjacent tent)\n",
				   x, y);
#endif
			soln[y*w+x] = NONTENT;
			done_something = true;
		    }
		}

	if (done_something)
	    continue;

	/*
	 * Any tree which has exactly one {unattached tent, BLANK}
	 * adjacent to it must have its tent in that square.
	 */
	for (y = 0; y < h; y++)
	    for (x = 0; x < w; x++)
		if (soln[y*w+x] == TREE && !sc->links[y*w+x]) {
		    int linkd = 0, linkd2 = 0, nd = 0;

		    for (d = 1; d < MAXDIR; d++) {
			int x2 = x + dx(d), y2 = y + dy(d);
			if (!(x2 >= 0 && x2 < w && y2 >= 0 && y2 < h))
			    continue;
			if (soln[y2*w+x2] == BLANK ||
			    (soln[y2*w+x2] == TENT && !sc->links[y2*w+x2])) {
			    if (linkd)
				linkd2 = d;
			    else
				linkd = d;
			    nd++;
			}
		    }

		    if (nd == 0) {
#ifdef SOLVER_DIAGNOSTICS
			if (verbose)
			    printf("tree at %d,%d cannot link to anything\n",
				   x, y);
#endif
			return 0;      /* no solution exists */
		    } else if (nd == 1) {
			int x2 = x + dx(linkd), y2 = y + dy(linkd);

#ifdef SOLVER_DIAGNOSTICS
			if (verbose)
			    printf("tree at %d,%d can only link to tent at"
				   " %d,%d\n", x, y, x2, y2);
#endif
			soln[y2*w+x2] = TENT;
			sc->links[y*w+x] = linkd;
			sc->links[y2*w+x2] = F(linkd);
			done_something = true;
		    } else if (nd == 2 && (!dx(linkd) != !dx(linkd2)) &&
			       diff >= DIFF_TRICKY) {
			/*
			 * If there are two possible places where
			 * this tree's tent can go, and they are
			 * diagonally separated rather than being
			 * on opposite sides of the tree, then the
			 * square (other than the tree square)
			 * which is adjacent to both of them must
			 * be a non-tent.
			 */
			int x2 = x + dx(linkd) + dx(linkd2);
			int y2 = y + dy(linkd) + dy(linkd2);
			assert(x2 >= 0 && x2 < w && y2 >= 0 && y2 < h);
			if (soln[y2*w+x2] == BLANK) {
#ifdef SOLVER_DIAGNOSTICS
			    if (verbose)
				printf("possible tent locations for tree at"
				       " %d,%d rule out tent at %d,%d\n",
				       x, y, x2, y2);
#endif
			    soln[y2*w+x2] = NONTENT;
			    done_something = true;
			}
		    }
		}

	if (done_something)
	    continue;

	/*
	 * If localised deductions about the trees and tents
	 * themselves haven't helped us, it's time to resort to the
	 * numbers round the grid edge. For each row and column, we
	 * go through all possible combinations of locations for
	 * the unplaced tents, rule out any which have adjacent
	 * tents, and spot any square which is given the same state
	 * by all remaining combinations.
	 */
	for (i = 0; i < w+h; i++) {
	    int start, step, len, start1, start2, n, k;

	    if (i < w) {
		/*
		 * This is the number for a column.
		 */
		start = i;
		step = w;
		len = h;
		if (i > 0)
		    start1 = start - 1;
		else
		    start1 = -1;
		if (i+1 < w)
		    start2 = start + 1;
		else
		    start2 = -1;
	    } else {
		/*
		 * This is the number for a row.
		 */
		start = (i-w)*w;
		step = 1;
		len = w;
		if (i > w)
		    start1 = start - w;
		else
		    start1 = -1;
		if (i+1 < w+h)
		    start2 = start + w;
		else
		    start2 = -1;
	    }

	    if (diff < DIFF_TRICKY) {
		/*
		 * In Easy mode, we don't look at the effect of one
		 * row on the next (i.e. ruling out a square if all
		 * possibilities for an adjacent row place a tent
		 * next to it).
		 */
		start1 = start2 = -1;
	    }

	    k = numbers[i];

	    /*
	     * Count and store the locations of the free squares,
	     * and also count the number of tents already placed.
	     */
	    n = 0;
	    for (j = 0; j < len; j++) {
		if (soln[start+j*step] == TENT)
		    k--;	       /* one fewer tent to place */
		else if (soln[start+j*step] == BLANK)
		    sc->locs[n++] = j;
	    }

	    if (n == 0)
		continue;	       /* nothing left to do here */

	    /*
	     * Now we know we're placing k tents in n squares. Set
	     * up the first possibility.
	     */
	    for (j = 0; j < n; j++)
		sc->place[j] = (j < k ? TENT : NONTENT);

	    /*
	     * We're aiming to find squares in this row which are
	     * invariant over all valid possibilities. Thus, we
	     * maintain the current state of that invariance. We
	     * start everything off at MAGIC to indicate that it
	     * hasn't been set up yet.
	     */
	    mrow = sc->mrows;
	    trow = sc->trows;
	    trow1 = sc->trows + len;
	    trow2 = sc->trows + 2*len;
	    memset(mrow, MAGIC, 3*len);

	    /*
	     * And iterate over all possibilities.
	     */
	    while (1) {
		int p;
                bool valid;

		/*
		 * See if this possibility is valid. The only way
		 * it can fail to be valid is if it contains two
		 * adjacent tents. (Other forms of invalidity, such
		 * as containing a tent adjacent to one already
		 * placed, will have been dealt with already by
		 * other parts of the solver.)
		 */
		valid = true;
		for (j = 0; j+1 < n; j++)
		    if (sc->place[j] == TENT &&
			sc->place[j+1] == TENT &&
			sc->locs[j+1] == sc->locs[j]+1) {
			valid = false;
			break;
		    }

		if (valid) {
		    /*
		     * Merge this valid combination into mrow.
		     */
		    memset(trow, MAGIC, len);
		    memset(trow+len, BLANK, 2*len);
		    for (j = 0; j < n; j++) {
			trow[sc->locs[j]] = sc->place[j];
			if (sc->place[j] == TENT) {
			    int jj;
			    for (jj = sc->locs[j]-1; jj <= sc->locs[j]+1; jj++)
				if (jj >= 0 && jj < len)
				    trow1[jj] = trow2[jj] = NONTENT;
			}
		    }

		    for (j = 0; j < 3*len; j++) {
			if (trow[j] == MAGIC)
			    continue;
			if (mrow[j] == MAGIC || mrow[j] == trow[j]) {
			    /*
			     * Either this is the first valid
			     * placement we've found at all, or
			     * this square's contents are
			     * consistent with every previous valid
			     * combination.
			     */
			    mrow[j] = trow[j];
			} else {
			    /*
			     * This square's contents fail to match
			     * what they were in a different
			     * combination, so we cannot deduce
			     * anything about this square.
			     */
			    mrow[j] = BLANK;
			}
		    }
		}

		/*
		 * Find the next combination of k choices from n.
		 * We do this by finding the rightmost tent which
		 * can be moved one place right, doing so, and
		 * shunting all tents to the right of that as far
		 * left as they can go.
		 */
		p = 0;
		for (j = n-1; j > 0; j--) {
		    if (sc->place[j] == TENT)
			p++;
		    if (sc->place[j] == NONTENT && sc->place[j-1] == TENT) {
			sc->place[j-1] = NONTENT;
			sc->place[j] = TENT;
			while (p--)
			    sc->place[++j] = TENT;
			while (++j < n)
			    sc->place[j] = NONTENT;
			break;
		    }
		}
		if (j <= 0)
		    break;	       /* we've finished */
	    }

	    /*
	     * It's just possible that _no_ placement was valid, in
	     * which case we have an internally inconsistent
	     * puzzle.
	     */
	    if (mrow[sc->locs[0]] == MAGIC)
		return 0;	       /* inconsistent */

	    /*
	     * Now go through mrow and see if there's anything
	     * we've deduced which wasn't already mentioned in soln.
	     */
	    for (j = 0; j < len; j++) {
		int whichrow;

		for (whichrow = 0; whichrow < 3; whichrow++) {
		    char *mthis = mrow + whichrow * len;
		    int tstart = (whichrow == 0 ? start :
				  whichrow == 1 ? start1 : start2);
		    if (tstart >= 0 &&
			mthis[j] != MAGIC && mthis[j] != BLANK &&
			soln[tstart+j*step] == BLANK) {
			int pos = tstart+j*step;

#ifdef SOLVER_DIAGNOSTICS
			if (verbose)
			    printf("%s %d forces %s at %d,%d\n",
				   step==1 ? "row" : "column",
				   step==1 ? start/w : start,
				   mthis[j] == TENT ? "tent" : "non-tent",
				   pos % w, pos / w);
#endif
			soln[pos] = mthis[j];
			done_something = true;
		    }
		}
	    }
	}

	if (done_something)
	    continue;

	if (!done_something)
	    break;
    }

    /*
     * The solver has nothing further it can do. Return 1 if both
     * soln and sc->links are completely filled in, or 2 otherwise.
     */
    for (y = 0; y < h; y++)
	for (x = 0; x < w; x++) {
	    if (soln[y*w+x] == BLANK)
		return 2;
	    if (soln[y*w+x] != NONTENT && sc->links[y*w+x] == 0)
		return 2;
	}

    return 1;
}

static char *new_game_desc(const game_params *params_in, random_state *rs,
			   char **aux, bool interactive)
{
    game_params params_copy = *params_in; /* structure copy */
    game_params *params = &params_copy;
    int w = params->w, h = params->h;
    int ntrees = w * h / 5;
    char *grid = snewn(w*h, char);
    char *puzzle = snewn(w*h, char);
    int *numbers = snewn(w+h, int);
    char *soln = snewn(w*h, char);
    int *order = snewn(w*h, int);
    int *treemap = snewn(w*h, int);
    int maxedges = ntrees*4 + w*h;
    int *adjdata = snewn(maxedges, int);
    int **adjlists = snewn(ntrees, int *);
    int *adjsizes = snewn(ntrees, int);
    int *outr = snewn(4*ntrees, int);
    struct solver_scratch *sc = new_scratch(w, h);
    char *ret, *p;
    int i, j, nl, nr;
    int *adjptr;

    /*
     * Since this puzzle has many global deductions and doesn't
     * permit limited clue sets, generating grids for this puzzle
     * is hard enough that I see no better option than to simply
     * generate a solution and see if it's unique and has the
     * required difficulty. This turns out to be computationally
     * plausible as well.
     * 
     * We chose our tree count (hence also tent count) by dividing
     * the total grid area by five above. Why five? Well, w*h/4 is
     * the maximum number of tents you can _possibly_ fit into the
     * grid without violating the separation criterion, and to
     * achieve that you are constrained to a very small set of
     * possible layouts (the obvious one with a tent at every
     * (even,even) coordinate, and trivial variations thereon). So
     * if we reduce the tent count a bit more, we enable more
     * random-looking placement; 5 turns out to be a plausible
     * figure which yields sensible puzzles. Increasing the tent
     * count would give puzzles whose solutions were too regimented
     * and could be solved by the use of that knowledge (and would
     * also take longer to find a viable placement); decreasing it
     * would make the grids emptier and more boring.
     * 
     * Actually generating a grid is a matter of first placing the
     * tents, and then placing the trees by the use of matching.c
     * (finding a distinct square adjacent to every tent). We do it
     * this way round because otherwise satisfying the tent
     * separation condition would become onerous: most randomly
     * chosen tent layouts do not satisfy this condition, so we'd
     * have gone to a lot of work before finding that a candidate
     * layout was unusable. Instead, we place the tents first and
     * ensure they meet the separation criterion _before_ doing
     * lots of computation; this works much better.
     * 
     * This generation strategy can fail at many points, including
     * as early as tent placement (if you get a bad random order in
     * which to greedily try the grid squares, you won't even
     * manage to find enough mutually non-adjacent squares to put
     * the tents in). Then it can fail if matching.c doesn't manage
     * to find a good enough matching (i.e. the tent placements don't
     * admit any adequate tree placements); and finally it can fail
     * if the solver finds that the problem has the wrong
     * difficulty (including being actually non-unique). All of
     * these, however, are insufficiently frequent to cause
     * trouble.
     */

    if (params->diff > DIFF_EASY && params->w <= 4 && params->h <= 4)
	params->diff = DIFF_EASY;      /* downgrade to prevent tight loop */

    while (1) {
	/*
	 * Make a list of grid squares which we'll permute as we pick
	 * the tent locations.
         *
         * We'll also need to index all the potential tree squares,
         * i.e. the ones adjacent to the tents.
	 */
	for (i = 0; i < w*h; i++) {
	    order[i] = i;
	    treemap[i] = -1;
        }

	/*
	 * Place tents at random without making any two adjacent.
	 */
	memset(grid, BLANK, w*h);
	j = ntrees;
        nr = 0;
        /* Loop end condition: either j==0 (we've placed all the
         * tents), or the number of grid squares we have yet to try
         * is too few to fit the remaining tents into. */
	for (i = 0; j > 0 && i+j <= w*h; i++) {
            int which, x, y, d, tmp;
	    int dy, dx;
            bool ok = true;

            // in this file it is:
            which = i + random_upto(rs, w*h - i);
            // in nmay231 version it is:
            which = i + random_upto(rs, j);
            // END
            tmp = order[which];
            order[which] = order[i];
            order[i] = tmp;

	    x = order[i] % w;
            y = order[i] / w;

	    for (dy = -1; dy <= +1; dy++)
		for (dx = -1; dx <= +1; dx++)
		    if (x+dx >= 0 && x+dx < w &&
			y+dy >= 0 && y+dy < h &&
			grid[(y+dy)*w+(x+dx)] == TENT)
			ok = false;

	    if (ok) {
		grid[order[i]] = TENT;
                for (d = 1; d < MAXDIR; d++) {
                    int x2 = x + dx(d), y2 = y + dy(d);
                    if (x2 >= 0 && x2 < w && y2 >= 0 && y2 < h &&
                        treemap[y2*w+x2] == -1) {
                        treemap[y2*w+x2] = nr++;
                    }
                }
		j--;
	    }
	}
	if (j > 0)
	    continue;		       /* couldn't place all the tents */

	/*
	 * Build up the graph for matching.c.
	 */
        adjptr = adjdata;
        nl = 0;
	for (i = 0; i < w*h; i++) {
	    if (grid[i] == TENT) {
                int d, x = i % w, y = i / w;
                adjlists[nl] = adjptr;
                for (d = 1; d < MAXDIR; d++) {
                    int x2 = x + dx(d), y2 = y + dy(d);
                    if (x2 >= 0 && x2 < w && y2 >= 0 && y2 < h) {
                        assert(treemap[y2*w+x2] != -1);
                        *adjptr++ = treemap[y2*w+x2];
		    }
		}
                adjsizes[nl] = adjptr - adjlists[nl];
                nl++;
	    }
	}

	/*
	 * Call the matching algorithm to actually place the trees.
	 */
	j = matching(ntrees, nr, adjlists, adjsizes, rs, NULL, outr);

	if (j < ntrees)
	    continue;		       /* couldn't place all the trees */

	/*
	 * Fill in the trees in the grid, by cross-referencing treemap
	 * (which maps a grid square to its index as known to
	 * matching()) against the output from matching().
         *
         * Note that for these purposes we don't actually care _which_
         * tent each potential tree square is assigned to - we only
         * care whether it was assigned to any tent at all, in order
         * to decide whether to put a tree in it.
	 */
	for (i = 0; i < w*h; i++)
            if (treemap[i] != -1 && outr[treemap[i]] != -1)
		grid[i] = TREE;

	/*
	 * I think it looks ugly if there isn't at least one of
	 * _something_ (tent or tree) in each row and each column
	 * of the grid. This doesn't give any information away
	 * since a completely empty row/column is instantly obvious
	 * from the clues (it has no trees and a zero).
	 */
	for (i = 0; i < w; i++) {
	    for (j = 0; j < h; j++) {
		if (grid[j*w+i] != BLANK)
		    break;	       /* found something in this column */
	    }
	    if (j == h)
		break;		       /* found empty column */
	}
	if (i < w)
	    continue;		       /* a column was empty */

	for (j = 0; j < h; j++) {
	    for (i = 0; i < w; i++) {
		if (grid[j*w+i] != BLANK)
		    break;	       /* found something in this row */
	    }
	    if (i == w)
		break;		       /* found empty row */
	}
	if (j < h)
	    continue;		       /* a row was empty */

	/*
	 * Now set up the numbers round the edge.
	 */
	for (i = 0; i < w; i++) {
	    int n = 0;
	    for (j = 0; j < h; j++)
		if (grid[j*w+i] == TENT)
		    n++;
	    numbers[i] = n;
	}
	for (i = 0; i < h; i++) {
	    int n = 0;
	    for (j = 0; j < w; j++)
		if (grid[i*w+j] == TENT)
		    n++;
	    numbers[w+i] = n;
	}

	/*
	 * And now actually solve the puzzle, to see whether it's
	 * unique and has the required difficulty.
	 */
        for (i = 0; i < w*h; i++)
            puzzle[i] = grid[i] == TREE ? TREE : BLANK;
	i = tents_solve(w, h, puzzle, numbers, soln, sc, params->diff-1);
	j = tents_solve(w, h, puzzle, numbers, soln, sc, params->diff);

        /*
         * We expect solving with difficulty params->diff to have
         * succeeded (otherwise the problem is too hard), and
         * solving with diff-1 to have failed (otherwise it's too
         * easy).
         */
	if (i == 2 && j == 1)
	    break;
    }

    /*
     * That's it. Encode as a game ID.
     */
    ret = snewn((w+h)*40 + ntrees + (w*h)/26 + 1, char);
    p = ret;
    j = 0;
    for (i = 0; i <= w*h; i++) {
	bool c = (i < w*h ? grid[i] == TREE : true);
	if (c) {
	    *p++ = (j == 0 ? '_' : j-1 + 'a');
	    j = 0;
	} else {
	    j++;
	    while (j > 25) {
		*p++ = 'z';
		j -= 25;
	    }
	}
    }
    for (i = 0; i < w+h; i++)
	p += sprintf(p, ",%d", numbers[i]);
    *p++ = '\0';
    ret = sresize(ret, p - ret, char);

    /*
     * And encode the solution as an aux_info.
     */
    *aux = snewn(ntrees * 40, char);
    p = *aux;
    *p++ = 'S';
    for (i = 0; i < w*h; i++)
        if (grid[i] == TENT)
            p += sprintf(p, ";T%d,%d", i%w, i/w);
    *p++ = '\0';
    *aux = sresize(*aux, p - *aux, char);

    free_scratch(sc);
    sfree(outr);
    sfree(adjdata);
    sfree(adjlists);
    sfree(adjsizes);
    sfree(treemap);
    sfree(order);
    sfree(soln);
    sfree(numbers);
    sfree(puzzle);
    sfree(grid);

    return ret;
}

static const char *validate_desc(const game_params *params, const char *desc)
{
    int w = params->w, h = params->h;
    int area, i;

    area = 0;
    while (*desc && *desc != ',') {
	if (*desc == '_')
            area++;
	else if (*desc >= 'a' && *desc < 'z')
            area += *desc - 'a' + 2;
	else if (*desc == 'z')
            area += 25;
        else if (*desc == '!' || *desc == '-')
            /* do nothing */;
        else
            return "Invalid character in grid specification";

	desc++;
    }
    if (area < w * h + 1)
	return "Not enough data to fill grid";
    else if (area > w * h + 1)
	return "Too much data to fill grid";

    for (i = 0; i < w+h; i++) {
	if (!*desc)
            return "Not enough numbers given after grid specification";
        else if (*desc != ',')
            return "Invalid character in number list";
	desc++;
	while (*desc && isdigit((unsigned char)*desc)) desc++;
    }

    if (*desc)
        return "Unexpected additional data at end of game description";
    return NULL;
}

static game_state *new_game(midend *me, const game_params *params,
                            const char *desc)
{
    int w = params->w, h = params->h;
    game_state *state = snew(game_state);
    int i;

    state->p = *params;		       /* structure copy */
    state->grid = snewn(w*h, char);
    state->numbers = snew(struct numbers);
    state->numbers->refcount = 1;
    state->numbers->numbers = snewn(w+h, int);
    state->completed = state->used_solve = false;

    i = 0;
    memset(state->grid, BLANK, w*h);

    while (*desc) {
	int run, type;

	type = TREE;

	if (*desc == '_')
	    run = 0;
	else if (*desc >= 'a' && *desc < 'z')
	    run = *desc - ('a'-1);
	else if (*desc == 'z') {
	    run = 25;
	    type = BLANK;
	} else {
	    assert(*desc == '!' || *desc == '-');
	    run = -1;
	    type = (*desc == '!' ? TENT : NONTENT);
	}

	desc++;

	i += run;
	assert(i >= 0 && i <= w*h);
	if (i == w*h) {
	    assert(type == TREE);
	    break;
	} else {
	    if (type != BLANK)
		state->grid[i++] = type;
	}
    }

    for (i = 0; i < w+h; i++) {
	assert(*desc == ',');
	desc++;
	state->numbers->numbers[i] = atoi(desc);
	while (*desc && isdigit((unsigned char)*desc)) desc++;
    }

    assert(!*desc);

    return state;
}

static game_state *dup_game(const game_state *state)
{
    int w = state->p.w, h = state->p.h;
    game_state *ret = snew(game_state);

    ret->p = state->p;		       /* structure copy */
    ret->grid = snewn(w*h, char);
    memcpy(ret->grid, state->grid, w*h);
    ret->numbers = state->numbers;
    state->numbers->refcount++;
    ret->completed = state->completed;
    ret->used_solve = state->used_solve;

    return ret;
}

static void free_game(game_state *state)
{
    if (--state->numbers->refcount <= 0) {
	sfree(state->numbers->numbers);
	sfree(state->numbers);
    }
    sfree(state->grid);
    sfree(state);
}

static char *solve_game(const game_state *state, const game_state *currstate,
                        const char *aux, const char **error)
{
    int w = state->p.w, h = state->p.h;

    if (aux) {
	/*
	 * If we already have the solution, save ourselves some
	 * time.
	 */
        return dupstr(aux);
    } else {
	struct solver_scratch *sc = new_scratch(w, h);
        char *soln;
        int ret;
        char *move, *p;
        int i;

	soln = snewn(w*h, char);
	ret = tents_solve(w, h, state->grid, state->numbers->numbers,
                          soln, sc, DIFFCOUNT-1);
	free_scratch(sc);
	if (ret != 1) {
	    sfree(soln);
	    if (ret == 0)
		*error = "This puzzle is not self-consistent";
	    else
		*error = "Unable to find a unique solution for this puzzle";
            return NULL;
	}

        /*
         * Construct a move string which turns the current state
         * into the solved state.
         */
        move = snewn(w*h * 40, char);
        p = move;
        *p++ = 'S';
        for (i = 0; i < w*h; i++)
            if (soln[i] == TENT)
                p += sprintf(p, ";T%d,%d", i%w, i/w);
        *p++ = '\0';
        move = sresize(move, p - move, char);

	sfree(soln);

        return move;
    }
}

static bool game_can_format_as_text_now(const game_params *params)
{
    return params->w <= 1998 && params->h <= 1998; /* 999 tents */
}

static char *game_text_format(const game_state *state)
{
    int w = state->p.w, h = state->p.h, r, c;
    int cw = 4, ch = 2, gw = (w+1)*cw + 2, gh = (h+1)*ch + 1, len = gw * gh;
    char *board = snewn(len + 1, char);

    sprintf(board, "%*s\n", len - 2, "");
    for (r = 0; r <= h; ++r) {
	for (c = 0; c <= w; ++c) {
	    int cell = r*ch*gw + cw*c, center = cell + gw*ch/2 + cw/2;
	    int i = r*w + c, n = 1000;

	    if (r == h && c == w) /* NOP */;
	    else if (c == w) n = state->numbers->numbers[w + r];
	    else if (r == h) n = state->numbers->numbers[c];
	    else switch (state->grid[i]) {
		case BLANK: board[center] = '.'; break;
		case TREE: board[center] = 'T'; break;
		case TENT: memcpy(board + center - 1, "//\\", 3); break;
		case NONTENT: break;
		default: memcpy(board + center - 1, "wtf", 3);
		}

	    if (n < 100) {
                board[center] = '0' + n % 10;
                if (n >= 10) board[center - 1] = '0' + n / 10;
            } else if (n < 1000) {
                board[center + 1] = '0' + n % 10;
                board[center] = '0' + n / 10 % 10;
                board[center - 1] = '0' + n / 100;
	    }

	    board[cell] = '+';
	    memset(board + cell + 1, '-', cw - 1);
	    for (i = 1; i < ch; ++i) board[cell + i*gw] = '|';
	}

	for (c = 0; c < ch; ++c) {
	    board[(r*ch+c)*gw + gw - 2] =
		c == 0 ? '+' : r < h ? '|' : ' ';
	    board[(r*ch+c)*gw + gw - 1] = '\n';
	}
    }

    memset(board + len - gw, '-', gw - 2 - cw);
    for (c = 0; c <= w; ++c) board[len - gw + cw*c] = '+';

    return board;
}

struct game_ui {
    int dsx, dsy;                      /* coords of drag start */
    int dex, dey;                      /* coords of drag end */
    int drag_button;                   /* -1 for none, or a button code */
    bool drag_ok;                      /* dragged off the window, to cancel */

    int cx, cy;                        /* cursor position. */
    bool cdisp;                        /* is cursor displayed? */
};

static game_ui *new_ui(const game_state *state)
{
    game_ui *ui = snew(game_ui);
    ui->dsx = ui->dsy = -1;
    ui->dex = ui->dey = -1;
    ui->drag_button = -1;
    ui->drag_ok = false;
    ui->cx = ui->cy = 0;
    ui->cdisp = false;
    return ui;
}

static void free_ui(game_ui *ui)
{
    sfree(ui);
}

static char *encode_ui(const game_ui *ui)
{
    return NULL;
}

static void decode_ui(game_ui *ui, const char *encoding)
{
}

static void game_changed_state(game_ui *ui, const game_state *oldstate,
                               const game_state *newstate)
{
}

struct game_drawstate {
    int tilesize;
    bool started;
    game_params p;
    int *drawn, *numbersdrawn;
    int cx, cy;         /* last-drawn cursor pos, or (-1,-1) if absent. */
};

#define PREFERRED_TILESIZE 32
#define TILESIZE (ds->tilesize)
#define TLBORDER (TILESIZE/2)
#define BRBORDER (TILESIZE*3/2)
#define COORD(x)  ( (x) * TILESIZE + TLBORDER )
#define FROMCOORD(x)  ( ((x) - TLBORDER + TILESIZE) / TILESIZE - 1 )

#define FLASH_TIME 0.30F

static int drag_xform(const game_ui *ui, int x, int y, int v)
{
    int xmin, ymin, xmax, ymax;

    xmin = min(ui->dsx, ui->dex);
    xmax = max(ui->dsx, ui->dex);
    ymin = min(ui->dsy, ui->dey);
    ymax = max(ui->dsy, ui->dey);

#ifndef STYLUS_BASED
    /*
     * Left-dragging has no effect, so we treat a left-drag as a
     * single click on dsx,dsy.
     */
    if (ui->drag_button == LEFT_BUTTON) {
        xmin = xmax = ui->dsx;
        ymin = ymax = ui->dsy;
    }
#endif

    if (x < xmin || x > xmax || y < ymin || y > ymax)
        return v;                      /* no change outside drag area */

    if (v == TREE)
        return v;                      /* trees are inviolate always */

    if (xmin == xmax && ymin == ymax) {
        /*
         * Results of a simple click. Left button sets blanks to
         * tents; right button sets blanks to non-tents; either
         * button clears a non-blank square.
         * If stylus-based however, it loops instead.
         */
        if (ui->drag_button == LEFT_BUTTON)
#ifdef STYLUS_BASED
            v = (v == BLANK ? TENT : (v == TENT ? NONTENT : BLANK));
        else
            v = (v == BLANK ? NONTENT : (v == NONTENT ? TENT : BLANK));
#else
            v = (v == BLANK ? TENT : BLANK);
        else
            v = (v == BLANK ? NONTENT : BLANK);
#endif
    } else {
        /*
         * Results of a drag. Left-dragging has no effect.
         * Right-dragging sets all blank squares to non-tents and
         * has no effect on anything else.
         */
        if (ui->drag_button == RIGHT_BUTTON)
            v = (v == BLANK ? NONTENT : v);
        else
#ifdef STYLUS_BASED
            v = (v == BLANK ? NONTENT : v);
#else
            /* do nothing */;
#endif
    }

    return v;
}

static char *interpret_move(const game_state *state, game_ui *ui,
                            const game_drawstate *ds,
                            int x, int y, int button)
{
    int w = state->p.w, h = state->p.h;
    char tmpbuf[80];
    bool shift = button & MOD_SHFT, control = button & MOD_CTRL;

    button &= ~MOD_MASK;

    if (button == LEFT_BUTTON || button == RIGHT_BUTTON) {
        x = FROMCOORD(x);
        y = FROMCOORD(y);
        if (x < 0 || y < 0 || x >= w || y >= h)
            return NULL;

        ui->drag_button = button;
        ui->dsx = ui->dex = x;
        ui->dsy = ui->dey = y;
        ui->drag_ok = true;
        ui->cdisp = false;
        return UI_UPDATE;
    }

    if ((IS_MOUSE_DRAG(button) || IS_MOUSE_RELEASE(button)) &&
        ui->drag_button > 0) {
        int xmin, ymin, xmax, ymax;
        char *buf;
        const char *sep;
        int buflen, bufsize, tmplen;

        x = FROMCOORD(x);
        y = FROMCOORD(y);
        if (x < 0 || y < 0 || x >= w || y >= h) {
            ui->drag_ok = false;
        } else {
            /*
             * Drags are limited to one row or column. Hence, we
             * work out which coordinate is closer to the drag
             * start, and move it _to_ the drag start.
             */
            if (abs(x - ui->dsx) < abs(y - ui->dsy))
                x = ui->dsx;
            else
                y = ui->dsy;

            ui->dex = x;
            ui->dey = y;

            ui->drag_ok = true;
        }

        if (IS_MOUSE_DRAG(button))
            return UI_UPDATE;

        /*
         * The drag has been released. Enact it.
         */
        if (!ui->drag_ok) {
            ui->drag_button = -1;
            return UI_UPDATE;          /* drag was just cancelled */
        }

        xmin = min(ui->dsx, ui->dex);
        xmax = max(ui->dsx, ui->dex);
        ymin = min(ui->dsy, ui->dey);
        ymax = max(ui->dsy, ui->dey);
        assert(0 <= xmin && xmin <= xmax && xmax < w);
        assert(0 <= ymin && ymin <= ymax && ymax < h);

        buflen = 0;
        bufsize = 256;
        buf = snewn(bufsize, char);
        sep = "";
        for (y = ymin; y <= ymax; y++)
            for (x = xmin; x <= xmax; x++) {
                int v = drag_xform(ui, x, y, state->grid[y*w+x]);
                if (state->grid[y*w+x] != v) {
                    tmplen = sprintf(tmpbuf, "%s%c%d,%d", sep,
                                     (int)(v == BLANK ? 'B' :
                                           v == TENT ? 'T' : 'N'),
                                     x, y);
                    sep = ";";

                    if (buflen + tmplen >= bufsize) {
                        bufsize = buflen + tmplen + 256;
                        buf = sresize(buf, bufsize, char);
                    }

                    strcpy(buf+buflen, tmpbuf);
                    buflen += tmplen;
                }
            }

        ui->drag_button = -1;          /* drag is terminated */

        if (buflen == 0) {
            sfree(buf);
            return UI_UPDATE;          /* drag was terminated */
        } else {
            buf[buflen] = '\0';
            return buf;
        }
    }

    if (IS_CURSOR_MOVE(button)) {
        ui->cdisp = true;
        if (shift || control) {
            int len = 0, i, indices[2];
            indices[0] = ui->cx + w * ui->cy;
            move_cursor(button, &ui->cx, &ui->cy, w, h, false);
            indices[1] = ui->cx + w * ui->cy;

            /* NONTENTify all unique traversed eligible squares */
            for (i = 0; i <= (indices[0] != indices[1]); ++i)
                if (state->grid[indices[i]] == BLANK ||
                    (control && state->grid[indices[i]] == TENT)) {
                    len += sprintf(tmpbuf + len, "%sN%d,%d", len ? ";" : "",
                                   indices[i] % w, indices[i] / w);
                    assert(len < lenof(tmpbuf));
                }

            tmpbuf[len] = '\0';
            if (len) return dupstr(tmpbuf);
        } else
            move_cursor(button, &ui->cx, &ui->cy, w, h, false);
        return UI_UPDATE;
    }
    if (ui->cdisp) {
        char rep = 0;
        int v = state->grid[ui->cy*w+ui->cx];

        if (v != TREE) {
#ifdef SINGLE_CURSOR_SELECT
            if (button == CURSOR_SELECT)
                /* SELECT cycles T, N, B */
                rep = v == BLANK ? 'T' : v == TENT ? 'N' : 'B';
#else
            if (button == CURSOR_SELECT)
                rep = v == BLANK ? 'T' : 'B';
            else if (button == CURSOR_SELECT2)
                rep = v == BLANK ? 'N' : 'B';
            else if (button == 'T' || button == 'N' || button == 'B')
                rep = (char)button;
#endif
        }

        if (rep) {
            sprintf(tmpbuf, "%c%d,%d", (int)rep, ui->cx, ui->cy);
            return dupstr(tmpbuf);
        }
    } else if (IS_CURSOR_SELECT(button)) {
        ui->cdisp = true;
        return UI_UPDATE;
    }

    return NULL;
}

static game_state *execute_move(const game_state *state, const char *move)
{
    int w = state->p.w, h = state->p.h;
    char c;
    int x, y, m, n, i, j;
    game_state *ret = dup_game(state);

    while (*move) {
        c = *move;
	if (c == 'S') {
            int i;
	    ret->used_solve = true;
            /*
             * Set all non-tree squares to NONTENT. The rest of the
             * solve move will fill the tents in over the top.
             */
            for (i = 0; i < w*h; i++)
                if (ret->grid[i] != TREE)
                    ret->grid[i] = NONTENT;
	    move++;
	} else if (c == 'B' || c == 'T' || c == 'N') {
            move++;
            if (sscanf(move, "%d,%d%n", &x, &y, &n) != 2 ||
                x < 0 || y < 0 || x >= w || y >= h) {
                free_game(ret);
                return NULL;
            }
            if (ret->grid[y*w+x] == TREE) {
                free_game(ret);
                return NULL;
            }
            ret->grid[y*w+x] = (c == 'B' ? BLANK : c == 'T' ? TENT : NONTENT);
            move += n;
        } else {
            free_game(ret);
            return NULL;
        }
        if (*move == ';')
            move++;
        else if (*move) {
            free_game(ret);
            return NULL;
        }
    }

    /*
     * Check for completion.
     */
    for (i = n = m = 0; i < w*h; i++) {
        if (ret->grid[i] == TENT)
            n++;
        else if (ret->grid[i] == TREE)
            m++;
    }
    if (n == m) {
        int *gridids, *adjdata, **adjlists, *adjsizes, *adjptr;

        /*
         * We have the right number of tents, which is a
         * precondition for the game being complete. Now check that
         * the numbers add up.
         */
	for (i = 0; i < w; i++) {
	    n = 0;
	    for (j = 0; j < h; j++)
		if (ret->grid[j*w+i] == TENT)
		    n++;
	    if (ret->numbers->numbers[i] != n)
                goto completion_check_done;
	}
	for (i = 0; i < h; i++) {
            n = 0;
	    for (j = 0; j < w; j++)
		if (ret->grid[i*w+j] == TENT)
		    n++;
	    if (ret->numbers->numbers[w+i] != n)
                goto completion_check_done;
	}
        /*
         * Also, check that no two tents are adjacent.
         */
        for (y = 0; y < h; y++)
            for (x = 0; x < w; x++) {
                if (x+1 < w &&
                    ret->grid[y*w+x] == TENT && ret->grid[y*w+x+1] == TENT)
                    goto completion_check_done;
                if (y+1 < h &&
                    ret->grid[y*w+x] == TENT && ret->grid[(y+1)*w+x] == TENT)
                    goto completion_check_done;
                if (x+1 < w && y+1 < h) {
                    if (ret->grid[y*w+x] == TENT &&
                        ret->grid[(y+1)*w+(x+1)] == TENT)
                        goto completion_check_done;
                    if (ret->grid[(y+1)*w+x] == TENT &&
                        ret->grid[y*w+(x+1)] == TENT)
                        goto completion_check_done;
                }
            }

        /*
         * OK; we have the right number of tents, they match the
         * numeric clues, and they satisfy the non-adjacency
         * criterion. Finally, we need to verify that they can be
         * placed in a one-to-one matching with the trees such that
         * every tent is orthogonally adjacent to its tree.
         * 
         * This bit is where the hard work comes in: we have to do
         * it by finding such a matching using matching.c.
         */
        gridids = snewn(w*h, int);
        adjdata = snewn(m*4, int);
        adjlists = snewn(m, int *);
        adjsizes = snewn(m, int);

        /* Assign each tent and tree a consecutive vertex id for
         * matching(). */
        for (i = n = 0; i < w*h; i++) {
            if (ret->grid[i] == TENT)
                gridids[i] = n++;
        }
        assert(n == m);
        for (i = n = 0; i < w*h; i++) {
            if (ret->grid[i] == TREE)
                gridids[i] = n++;
        }
        assert(n == m);

        /* Build the vertices' adjacency lists. */
        adjptr = adjdata;
        for (y = 0; y < h; y++)
            for (x = 0; x < w; x++)
                if (ret->grid[y*w+x] == TREE) {
                    int d, treeid = gridids[y*w+x];
                    adjlists[treeid] = adjptr;

                    /*
                     * Here we use the direction enum declared for
                     * the solver. We make use of the fact that the
                     * directions are declared in the order
                     * U,L,R,D, meaning that we go through the four
                     * neighbours of any square in numerically
                     * increasing order.
                     */
		    for (d = 1; d < MAXDIR; d++) {
			int x2 = x + dx(d), y2 = y + dy(d);
			if (x2 >= 0 && x2 < w && y2 >= 0 && y2 < h &&
                            ret->grid[y2*w+x2] == TENT) {
                            *adjptr++ = gridids[y2*w+x2];
                        }
                    }
                    adjsizes[treeid] = adjptr - adjlists[treeid];
                }

	n = matching(m, m, adjlists, adjsizes, NULL, NULL, NULL);

        sfree(gridids);
        sfree(adjdata);
        sfree(adjlists);
        sfree(adjsizes);

        if (n != m)
            goto completion_check_done;

        /*
         * We haven't managed to fault the grid on any count. Score!
         */
        ret->completed = true;
    }
    completion_check_done:

    return ret;
}

/* ----------------------------------------------------------------------
 * Drawing routines.
 */

static void game_compute_size(const game_params *params, int tilesize,
                              int *x, int *y)
{
    /* fool the macros */
    struct dummy { int tilesize; } dummy, *ds = &dummy;
    dummy.tilesize = tilesize;

    *x = TLBORDER + BRBORDER + TILESIZE * params->w;
    *y = TLBORDER + BRBORDER + TILESIZE * params->h;
}

static void game_set_size(drawing *dr, game_drawstate *ds,
                          const game_params *params, int tilesize)
{
    ds->tilesize = tilesize;
}

static float *game_colours(frontend *fe, int *ncolours)
{
    float *ret = snewn(3 * NCOLOURS, float);

    frontend_default_colour(fe, &ret[COL_BACKGROUND * 3]);

    ret[COL_GRID * 3 + 0] = 0.0F;
    ret[COL_GRID * 3 + 1] = 0.0F;
    ret[COL_GRID * 3 + 2] = 0.0F;

    ret[COL_GRASS * 3 + 0] = 0.7F;
    ret[COL_GRASS * 3 + 1] = 1.0F;
    ret[COL_GRASS * 3 + 2] = 0.5F;

    ret[COL_TREETRUNK * 3 + 0] = 0.6F;
    ret[COL_TREETRUNK * 3 + 1] = 0.4F;
    ret[COL_TREETRUNK * 3 + 2] = 0.0F;

    ret[COL_TREELEAF * 3 + 0] = 0.0F;
    ret[COL_TREELEAF * 3 + 1] = 0.7F;
    ret[COL_TREELEAF * 3 + 2] = 0.0F;

    ret[COL_TENT * 3 + 0] = 0.8F;
    ret[COL_TENT * 3 + 1] = 0.7F;
    ret[COL_TENT * 3 + 2] = 0.0F;

    ret[COL_ERROR * 3 + 0] = 1.0F;
    ret[COL_ERROR * 3 + 1] = 0.0F;
    ret[COL_ERROR * 3 + 2] = 0.0F;

    ret[COL_ERRTEXT * 3 + 0] = 1.0F;
    ret[COL_ERRTEXT * 3 + 1] = 1.0F;
    ret[COL_ERRTEXT * 3 + 2] = 1.0F;

    ret[COL_ERRTRUNK * 3 + 0] = 0.6F;
    ret[COL_ERRTRUNK * 3 + 1] = 0.0F;
    ret[COL_ERRTRUNK * 3 + 2] = 0.0F;

    *ncolours = NCOLOURS;
    return ret;
}

static game_drawstate *game_new_drawstate(drawing *dr, const game_state *state)
{
    int w = state->p.w, h = state->p.h;
    struct game_drawstate *ds = snew(struct game_drawstate);
    int i;

    ds->tilesize = 0;
    ds->started = false;
    ds->p = state->p;                  /* structure copy */
    ds->drawn = snewn(w*h, int);
    for (i = 0; i < w*h; i++)
	ds->drawn[i] = MAGIC;
    ds->numbersdrawn = snewn(w+h, int);
    for (i = 0; i < w+h; i++)
	ds->numbersdrawn[i] = 2;
    ds->cx = ds->cy = -1;

    return ds;
}

static void game_free_drawstate(drawing *dr, game_drawstate *ds)
{
    sfree(ds->drawn);
    sfree(ds->numbersdrawn);
    sfree(ds);
}

enum {
    ERR_ADJ_TOPLEFT = 4,
    ERR_ADJ_TOP,
    ERR_ADJ_TOPRIGHT,
    ERR_ADJ_LEFT,
    ERR_ADJ_RIGHT,
    ERR_ADJ_BOTLEFT,
    ERR_ADJ_BOT,
    ERR_ADJ_BOTRIGHT,
    ERR_OVERCOMMITTED
};

static int *find_errors(const game_state *state, char *grid)
{
    int w = state->p.w, h = state->p.h;
    int *ret = snewn(w*h + w + h, int);
    int *tmp = snewn(w*h*2, int), *dsf = tmp + w*h;
    int x, y;

    /*
     * This function goes through a grid and works out where to
     * highlight play errors in red. The aim is that it should
     * produce at least one error highlight for any complete grid
     * (or complete piece of grid) violating a puzzle constraint, so
     * that a grid containing no BLANK squares is either a win or is
     * marked up in some way that indicates why not.
     *
     * So it's easy enough to highlight errors in the numeric clues
     * - just light up any row or column number which is not
     * fulfilled - and it's just as easy to highlight adjacent
     * tents. The difficult bit is highlighting failures in the
     * tent/tree matching criterion.
     *
     * A natural approach would seem to be to apply the matching.c
     * algorithm to find the tent/tree matching; if this fails, it
     * could be made to produce as a by-product some set of trees
     * which have too few tents between them (or vice versa). However,
     * it's bad for localising errors, because it's not easy to make
     * the algorithm narrow down to the _smallest_ such set of trees:
     * if trees A and B have only one tent between them, for instance,
     * it might perfectly well highlight not only A and B but also
     * trees C and D which are correctly matched on the far side of
     * the grid, on the grounds that those four trees between them
     * have only three tents.
     *
     * Also, that approach fares badly when you introduce the
     * additional requirement that incomplete grids should have
     * errors highlighted only when they can be proved to be errors
     * - so that trees should not be marked as having too few tents
     * if there are enough BLANK squares remaining around them that
     * could be turned into the missing tents (to do so would be
     * patronising, since the overwhelming likelihood is not that
     * the player has forgotten to put a tree there but that they
     * have merely not put one there _yet_). However, tents with too
     * few trees can be marked immediately, since those are
     * definitely player error.
     *
     * So I adopt an alternative approach, which is to consider the
     * bipartite adjacency graph between trees and tents
     * ('bipartite' in the sense that for these purposes I
     * deliberately ignore two adjacent trees or two adjacent
     * tents), divide that graph up into its connected components
     * using a dsf, and look for components which contain different
     * numbers of trees and tents. This allows me to highlight
     * groups of tents with too few trees between them immediately,
     * and then in order to find groups of trees with too few tents
     * I redo the same process but counting BLANKs as potential
     * tents (so that the only trees highlighted are those
     * surrounded by enough NONTENTs to make it impossible to give
     * them enough tents).
     *
     * However, this technique is incomplete: it is not a sufficient
     * condition for the existence of a perfect matching that every
     * connected component of the graph has the same number of tents
     * and trees. An example of a graph which satisfies the latter
     * condition but still has no perfect matching is
     * 
     *     A    B    C
     *     |   /   ,/|
     *     |  /  ,'/ |
     *     | / ,' /  |
     *     |/,'  /   |
     *     1    2    3
     *
     * which can be realised in Tents as
     * 
     *       B
     *     A 1 C 2
     *         3
     *
     * The matching-error highlighter described above will not mark
     * this construction as erroneous. However, something else will:
     * the three tents in the above diagram (let us suppose A,B,C
     * are the tents, though it doesn't matter which) contain two
     * diagonally adjacent pairs. So there will be _an_ error
     * highlighted for the above layout, even though not all types
     * of error will be highlighted.
     *
     * And in fact we can prove that this will always be the case:
     * that the shortcomings of the matching-error highlighter will
     * always be made up for by the easy tent adjacency highlighter.
     *
     * Lemma: Let G be a bipartite graph between n trees and n
     * tents, which is connected, and in which no tree has degree
     * more than two (but a tent may). Then G has a perfect matching.
     * 
     * (Note: in the statement and proof of the Lemma I will
     * consistently use 'tree' to indicate a type of graph vertex as
     * opposed to a tent, and not to indicate a tree in the graph-
     * theoretic sense.)
     *
     * Proof:
     * 
     * If we can find a tent of degree 1 joined to a tree of degree
     * 2, then any perfect matching must pair that tent with that
     * tree. Hence, we can remove both, leaving a smaller graph G'
     * which still satisfies all the conditions of the Lemma, and
     * which has a perfect matching iff G does.
     *
     * So, wlog, we may assume G contains no tent of degree 1 joined
     * to a tree of degree 2; if it does, we can reduce it as above.
     *
     * If G has no tent of degree 1 at all, then every tent has
     * degree at least two, so there are at least 2n edges in the
     * graph. But every tree has degree at most two, so there are at
     * most 2n edges. Hence there must be exactly 2n edges, so every
     * tree and every tent must have degree exactly two, which means
     * that the whole graph consists of a single loop (by
     * connectedness), and therefore certainly has a perfect
     * matching.
     *
     * Alternatively, if G does have a tent of degree 1 but it is
     * not connected to a tree of degree 2, then the tree it is
     * connected to must have degree 1 - and, by connectedness, that
     * must mean that that tent and that tree between them form the
     * entire graph. This trivial graph has a trivial perfect
     * matching. []
     *
     * That proves the lemma. Hence, in any case where the matching-
     * error highlighter fails to highlight an erroneous component
     * (because it has the same number of tents as trees, but they
     * cannot be matched up), the above lemma tells us that there
     * must be a tree with degree more than 2, i.e. a tree
     * orthogonally adjacent to at least three tents. But in that
     * case, there must be some pair of those three tents which are
     * diagonally adjacent to each other, so the tent-adjacency
     * highlighter will necessarily show an error. So any filled
     * layout in Tents which is not a correct solution to the puzzle
     * must have _some_ error highlighted by the subroutine below.
     *
     * (Of course it would be nicer if we could highlight all
     * errors: in the above example layout, we would like to
     * highlight tents A,B as having too few trees between them, and
     * trees 2,3 as having too few tents, in addition to marking the
     * adjacency problems. But I can't immediately think of any way
     * to find the smallest sets of such tents and trees without an
     * O(2^N) loop over all subsets of a given component.)
     */

    /*
     * ret[0] through to ret[w*h-1] give error markers for the grid
     * squares. After that, ret[w*h] to ret[w*h+w-1] give error
     * markers for the column numbers, and ret[w*h+w] to
     * ret[w*h+w+h-1] for the row numbers.
     */

    /*
     * Spot tent-adjacency violations.
     */
    for (x = 0; x < w*h; x++)
	ret[x] = 0;
    for (y = 0; y < h; y++) {
	for (x = 0; x < w; x++) {
	    if (y+1 < h && x+1 < w &&
		((grid[y*w+x] == TENT &&
		  grid[(y+1)*w+(x+1)] == TENT) ||
		 (grid[(y+1)*w+x] == TENT &&
		  grid[y*w+(x+1)] == TENT))) {
		ret[y*w+x] |= 1 << ERR_ADJ_BOTRIGHT;
		ret[(y+1)*w+x] |= 1 << ERR_ADJ_TOPRIGHT;
		ret[y*w+(x+1)] |= 1 << ERR_ADJ_BOTLEFT;
		ret[(y+1)*w+(x+1)] |= 1 << ERR_ADJ_TOPLEFT;
	    }
	    if (y+1 < h &&
		grid[y*w+x] == TENT &&
		grid[(y+1)*w+x] == TENT) {
		ret[y*w+x] |= 1 << ERR_ADJ_BOT;
		ret[(y+1)*w+x] |= 1 << ERR_ADJ_TOP;
	    }
	    if (x+1 < w &&
		grid[y*w+x] == TENT &&
		grid[y*w+(x+1)] == TENT) {
		ret[y*w+x] |= 1 << ERR_ADJ_RIGHT;
		ret[y*w+(x+1)] |= 1 << ERR_ADJ_LEFT;
	    }
	}
    }

    /*
     * Spot numeric clue violations.
     */
    for (x = 0; x < w; x++) {
	int tents = 0, maybetents = 0;
	for (y = 0; y < h; y++) {
	    if (grid[y*w+x] == TENT)
		tents++;
	    else if (grid[y*w+x] == BLANK)
		maybetents++;
	}
	ret[w*h+x] = (tents > state->numbers->numbers[x] ||
		      tents + maybetents < state->numbers->numbers[x]);
    }
    for (y = 0; y < h; y++) {
	int tents = 0, maybetents = 0;
	for (x = 0; x < w; x++) {
	    if (grid[y*w+x] == TENT)
		tents++;
	    else if (grid[y*w+x] == BLANK)
		maybetents++;
	}
	ret[w*h+w+y] = (tents > state->numbers->numbers[w+y] ||
			tents + maybetents < state->numbers->numbers[w+y]);
    }

    /*
     * Identify groups of tents with too few trees between them,
     * which we do by constructing the connected components of the
     * bipartite adjacency graph between tents and trees
     * ('bipartite' in the sense that we deliberately ignore
     * adjacency between tents or between trees), and highlighting
     * all the tents in any component which has a smaller tree
     * count.
     */
    dsf_init(dsf, w*h);
    /* Construct the equivalence classes. */
    for (y = 0; y < h; y++) {
	for (x = 0; x < w-1; x++) {
	    if ((grid[y*w+x] == TREE && grid[y*w+x+1] == TENT) ||
		(grid[y*w+x] == TENT && grid[y*w+x+1] == TREE))
		dsf_merge(dsf, y*w+x, y*w+x+1);
	}
    }
    for (y = 0; y < h-1; y++) {
	for (x = 0; x < w; x++) {
	    if ((grid[y*w+x] == TREE && grid[(y+1)*w+x] == TENT) ||
		(grid[y*w+x] == TENT && grid[(y+1)*w+x] == TREE))
		dsf_merge(dsf, y*w+x, (y+1)*w+x);
	}
    }
    /* Count up the tent/tree difference in each one. */
    for (x = 0; x < w*h; x++)
	tmp[x] = 0;
    for (x = 0; x < w*h; x++) {
	y = dsf_canonify(dsf, x);
	if (grid[x] == TREE)
	    tmp[y]++;
	else if (grid[x] == TENT)
	    tmp[y]--;
    }
    /* And highlight any tent belonging to an equivalence class with
     * a score less than zero. */
    for (x = 0; x < w*h; x++) {
	y = dsf_canonify(dsf, x);
	if (grid[x] == TENT && tmp[y] < 0)
	    ret[x] |= 1 << ERR_OVERCOMMITTED;
    }

    /*
     * Identify groups of trees with too few tents between them.
     * This is done similarly, except that we now count BLANK as
     * equivalent to TENT, i.e. we only highlight such trees when
     * the user hasn't even left _room_ to provide tents for them
     * all. (Otherwise, we'd highlight all trees red right at the
     * start of the game, before the user had done anything wrong!)
     */
#define TENT(x) ((x)==TENT || (x)==BLANK)
    dsf_init(dsf, w*h);
    /* Construct the equivalence classes. */
    for (y = 0; y < h; y++) {
	for (x = 0; x < w-1; x++) {
	    if ((grid[y*w+x] == TREE && TENT(grid[y*w+x+1])) ||
		(TENT(grid[y*w+x]) && grid[y*w+x+1] == TREE))
		dsf_merge(dsf, y*w+x, y*w+x+1);
	}
    }
    for (y = 0; y < h-1; y++) {
	for (x = 0; x < w; x++) {
	    if ((grid[y*w+x] == TREE && TENT(grid[(y+1)*w+x])) ||
		(TENT(grid[y*w+x]) && grid[(y+1)*w+x] == TREE))
		dsf_merge(dsf, y*w+x, (y+1)*w+x);
	}
    }
    /* Count up the tent/tree difference in each one. */
    for (x = 0; x < w*h; x++)
	tmp[x] = 0;
    for (x = 0; x < w*h; x++) {
	y = dsf_canonify(dsf, x);
	if (grid[x] == TREE)
	    tmp[y]++;
	else if (TENT(grid[x]))
	    tmp[y]--;
    }
    /* And highlight any tree belonging to an equivalence class with
     * a score more than zero. */
    for (x = 0; x < w*h; x++) {
	y = dsf_canonify(dsf, x);
	if (grid[x] == TREE && tmp[y] > 0)
	    ret[x] |= 1 << ERR_OVERCOMMITTED;
    }
#undef TENT

    sfree(tmp);
    return ret;
}

static void draw_err_adj(drawing *dr, game_drawstate *ds, int x, int y)
{
    int coords[8];
    int yext, xext;

    /*
     * Draw a diamond.
     */
    coords[0] = x - TILESIZE*2/5;
    coords[1] = y;
    coords[2] = x;
    coords[3] = y - TILESIZE*2/5;
    coords[4] = x + TILESIZE*2/5;
    coords[5] = y;
    coords[6] = x;
    coords[7] = y + TILESIZE*2/5;
    draw_polygon(dr, coords, 4, COL_ERROR, COL_GRID);

    /*
     * Draw an exclamation mark in the diamond. This turns out to
     * look unpleasantly off-centre if done via draw_text, so I do
     * it by hand on the basis that exclamation marks aren't that
     * difficult to draw...
     */
    xext = TILESIZE/16;
    yext = TILESIZE*2/5 - (xext*2+2);
    draw_rect(dr, x-xext, y-yext, xext*2+1, yext*2+1 - (xext*3),
	      COL_ERRTEXT);
    draw_rect(dr, x-xext, y+yext-xext*2+1, xext*2+1, xext*2, COL_ERRTEXT);
}

static void draw_tile(drawing *dr, game_drawstate *ds,
                      int x, int y, int v, bool cur, bool printing)
{
    int err;
    int tx = COORD(x), ty = COORD(y);
    int cx = tx + TILESIZE/2, cy = ty + TILESIZE/2;

    err = v & ~15;
    v &= 15;

    clip(dr, tx, ty, TILESIZE, TILESIZE);

    if (!printing) {
	draw_rect(dr, tx, ty, TILESIZE, TILESIZE, COL_GRID);
	draw_rect(dr, tx+1, ty+1, TILESIZE-1, TILESIZE-1,
		  (v == BLANK ? COL_BACKGROUND : COL_GRASS));
    }

    if (v == TREE) {
	int i;

	(printing ? draw_rect_outline : draw_rect)
	(dr, cx-TILESIZE/15, ty+TILESIZE*3/10,
	 2*(TILESIZE/15)+1, (TILESIZE*9/10 - TILESIZE*3/10),
	 (err & (1<<ERR_OVERCOMMITTED) ? COL_ERRTRUNK : COL_TREETRUNK));

	for (i = 0; i < (printing ? 2 : 1); i++) {
	    int col = (i == 1 ? COL_BACKGROUND :
		       (err & (1<<ERR_OVERCOMMITTED) ? COL_ERROR : 
			COL_TREELEAF));
	    int sub = i * (TILESIZE/32);
	    draw_circle(dr, cx, ty+TILESIZE*4/10, TILESIZE/4 - sub,
			col, col);
	    draw_circle(dr, cx+TILESIZE/5, ty+TILESIZE/4, TILESIZE/8 - sub,
			col, col);
	    draw_circle(dr, cx-TILESIZE/5, ty+TILESIZE/4, TILESIZE/8 - sub,
			col, col);
	    draw_circle(dr, cx+TILESIZE/4, ty+TILESIZE*6/13, TILESIZE/8 - sub,
			col, col);
	    draw_circle(dr, cx-TILESIZE/4, ty+TILESIZE*6/13, TILESIZE/8 - sub,
			col, col);
	}
    } else if (v == TENT) {
        int coords[6];
	int col;
        coords[0] = cx - TILESIZE/3;
        coords[1] = cy + TILESIZE/3;
        coords[2] = cx + TILESIZE/3;
        coords[3] = cy + TILESIZE/3;
        coords[4] = cx;
        coords[5] = cy - TILESIZE/3;
	col = (err & (1<<ERR_OVERCOMMITTED) ? COL_ERROR : COL_TENT);
        draw_polygon(dr, coords, 3, (printing ? -1 : col), col);
    }

    if (err & (1 << ERR_ADJ_TOPLEFT))
	draw_err_adj(dr, ds, tx, ty);
    if (err & (1 << ERR_ADJ_TOP))
	draw_err_adj(dr, ds, tx+TILESIZE/2, ty);
    if (err & (1 << ERR_ADJ_TOPRIGHT))
	draw_err_adj(dr, ds, tx+TILESIZE, ty);
    if (err & (1 << ERR_ADJ_LEFT))
	draw_err_adj(dr, ds, tx, ty+TILESIZE/2);
    if (err & (1 << ERR_ADJ_RIGHT))
	draw_err_adj(dr, ds, tx+TILESIZE, ty+TILESIZE/2);
    if (err & (1 << ERR_ADJ_BOTLEFT))
	draw_err_adj(dr, ds, tx, ty+TILESIZE);
    if (err & (1 << ERR_ADJ_BOT))
	draw_err_adj(dr, ds, tx+TILESIZE/2, ty+TILESIZE);
    if (err & (1 << ERR_ADJ_BOTRIGHT))
	draw_err_adj(dr, ds, tx+TILESIZE, ty+TILESIZE);

    if (cur) {
      int coff = TILESIZE/8;
      draw_rect_outline(dr, tx + coff, ty + coff,
                        TILESIZE - coff*2 + 1, TILESIZE - coff*2 + 1,
			COL_GRID);
    }

    unclip(dr);
    draw_update(dr, tx+1, ty+1, TILESIZE-1, TILESIZE-1);
}

/*
 * Internal redraw function, used for printing as well as drawing.
 */
static void int_redraw(drawing *dr, game_drawstate *ds,
                       const game_state *oldstate, const game_state *state,
                       int dir, const game_ui *ui,
		       float animtime, float flashtime, bool printing)
{
    int w = state->p.w, h = state->p.h;
    int x, y;
    bool flashing;
    int cx = -1, cy = -1;
    bool cmoved = false;
    char *tmpgrid;
    int *errors;

    if (ui) {
      if (ui->cdisp) { cx = ui->cx; cy = ui->cy; }
      if (cx != ds->cx || cy != ds->cy) cmoved = true;
    }

    if (printing || !ds->started) {
	if (printing)
	    print_line_width(dr, TILESIZE/64);

        /*
         * Draw the grid.
         */
        for (y = 0; y <= h; y++)
            draw_line(dr, COORD(0), COORD(y), COORD(w), COORD(y), COL_GRID);
        for (x = 0; x <= w; x++)
            draw_line(dr, COORD(x), COORD(0), COORD(x), COORD(h), COL_GRID);
    }

    if (flashtime > 0)
	flashing = (int)(flashtime * 3 / FLASH_TIME) != 1;
    else
	flashing = false;

    /*
     * Find errors. For this we use _part_ of the information from a
     * currently active drag: we transform dsx,dsy but not anything
     * else. (This seems to strike a good compromise between having
     * the error highlights respond instantly to single clicks, but
     * not giving constant feedback during a right-drag.)
     */
    if (ui && ui->drag_button >= 0) {
	tmpgrid = snewn(w*h, char);
	memcpy(tmpgrid, state->grid, w*h);
	tmpgrid[ui->dsy * w + ui->dsx] =
	    drag_xform(ui, ui->dsx, ui->dsy, tmpgrid[ui->dsy * w + ui->dsx]);
	errors = find_errors(state, tmpgrid);
	sfree(tmpgrid);
    } else {
	errors = find_errors(state, state->grid);
    }

    /*
     * Draw the grid.
     */
    for (y = 0; y < h; y++) {
        for (x = 0; x < w; x++) {
            int v = state->grid[y*w+x];
            bool credraw = false;

            /*
             * We deliberately do not take drag_ok into account
             * here, because user feedback suggests that it's
             * marginally nicer not to have the drag effects
             * flickering on and off disconcertingly.
             */
            if (ui && ui->drag_button >= 0)
                v = drag_xform(ui, x, y, v);

            if (flashing && (v == TREE || v == TENT))
                v = NONTENT;

            if (cmoved) {
              if ((x == cx && y == cy) ||
                  (x == ds->cx && y == ds->cy)) credraw = true;
            }

	    v |= errors[y*w+x];

            if (printing || ds->drawn[y*w+x] != v || credraw) {
                draw_tile(dr, ds, x, y, v, (x == cx && y == cy), printing);
                if (!printing)
		    ds->drawn[y*w+x] = v;
            }
        }
    }

    /*
     * Draw (or redraw, if their error-highlighted state has
     * changed) the numbers.
     */
    for (x = 0; x < w; x++) {
	if (printing || ds->numbersdrawn[x] != errors[w*h+x]) {
	    char buf[80];
	    draw_rect(dr, COORD(x), COORD(h)+1, TILESIZE, BRBORDER-1,
		      COL_BACKGROUND);
	    sprintf(buf, "%d", state->numbers->numbers[x]);
	    draw_text(dr, COORD(x) + TILESIZE/2, COORD(h+1),
		      FONT_VARIABLE, TILESIZE/2, ALIGN_HCENTRE|ALIGN_VNORMAL,
		      (errors[w*h+x] ? COL_ERROR : COL_GRID), buf);
	    draw_update(dr, COORD(x), COORD(h)+1, TILESIZE, BRBORDER-1);
	    if (!printing)
                ds->numbersdrawn[x] = errors[w*h+x];
	}
    }
    for (y = 0; y < h; y++) {
	if (printing || ds->numbersdrawn[w+y] != errors[w*h+w+y]) {
	    char buf[80];
	    draw_rect(dr, COORD(w)+1, COORD(y), BRBORDER-1, TILESIZE,
		      COL_BACKGROUND);
	    sprintf(buf, "%d", state->numbers->numbers[w+y]);
	    draw_text(dr, COORD(w+1), COORD(y) + TILESIZE/2,
		      FONT_VARIABLE, TILESIZE/2, ALIGN_HRIGHT|ALIGN_VCENTRE,
		      (errors[w*h+w+y] ? COL_ERROR : COL_GRID), buf);
	    draw_update(dr, COORD(w)+1, COORD(y), BRBORDER-1, TILESIZE);
	    if (!printing)
                ds->numbersdrawn[w+y] = errors[w*h+w+y];
	}
    }

    if (cmoved) {
	ds->cx = cx;
	ds->cy = cy;
    }

    sfree(errors);
}

static void game_redraw(drawing *dr, game_drawstate *ds,
                        const game_state *oldstate, const game_state *state,
                        int dir, const game_ui *ui,
                        float animtime, float flashtime)
{
    int_redraw(dr, ds, oldstate, state, dir, ui, animtime, flashtime, false);
}

static float game_anim_length(const game_state *oldstate,
                              const game_state *newstate, int dir, game_ui *ui)
{
    return 0.0F;
}

static float game_flash_length(const game_state *oldstate,
                               const game_state *newstate, int dir, game_ui *ui)
{
    if (!oldstate->completed && newstate->completed &&
	!oldstate->used_solve && !newstate->used_solve)
        return FLASH_TIME;

    return 0.0F;
}

static void game_get_cursor_location(const game_ui *ui,
                                     const game_drawstate *ds,
                                     const game_state *state,
                                     const game_params *params,
                                     int *x, int *y, int *w, int *h)
{
    if(ui->cdisp) {
        *x = COORD(ui->cx);
        *y = COORD(ui->cy);
        *w = *h = TILESIZE;
    }
}

static int game_status(const game_state *state)
{
    return state->completed ? +1 : 0;
}

static bool game_timing_state(const game_state *state, game_ui *ui)
{
    return true;
}

static void game_print_size(const game_params *params, float *x, float *y)
{
    int pw, ph;

    /*
     * I'll use 6mm squares by default.
     */
    game_compute_size(params, 600, &pw, &ph);
    *x = pw / 100.0F;
    *y = ph / 100.0F;
}

static void game_print(drawing *dr, const game_state *state, int tilesize)
{
    int c;

    /* Ick: fake up `ds->tilesize' for macro expansion purposes */
    game_drawstate ads, *ds = &ads;
    game_set_size(dr, ds, NULL, tilesize);

    c = print_mono_colour(dr, 1); assert(c == COL_BACKGROUND);
    c = print_mono_colour(dr, 0); assert(c == COL_GRID);
    c = print_mono_colour(dr, 1); assert(c == COL_GRASS);
    c = print_mono_colour(dr, 0); assert(c == COL_TREETRUNK);
    c = print_mono_colour(dr, 0); assert(c == COL_TREELEAF);
    c = print_mono_colour(dr, 0); assert(c == COL_TENT);

    int_redraw(dr, ds, NULL, state, +1, NULL, 0.0F, 0.0F, true);
}

#ifdef COMBINED
#define thegame tents
#endif

const struct game thegame = {
    "Tents", "games.tents", "tents",
    default_params,
    game_fetch_preset, NULL,
    decode_params,
    encode_params,
    free_params,
    dup_params,
    true, game_configure, custom_params,
    validate_params,
    new_game_desc,
    validate_desc,
    new_game,
    dup_game,
    free_game,
    true, solve_game,
    true, game_can_format_as_text_now, game_text_format,
    new_ui,
    free_ui,
    encode_ui,
    decode_ui,
    NULL, /* game_request_keys */
    game_changed_state,
    interpret_move,
    execute_move,
    PREFERRED_TILESIZE, game_compute_size, game_set_size,
    game_colours,
    game_new_drawstate,
    game_free_drawstate,
    game_redraw,
    game_anim_length,
    game_flash_length,
    game_get_cursor_location,
    game_status,
    true, false, game_print_size, game_print,
    false,			       /* wants_statusbar */
    false, game_timing_state,
    REQUIRE_RBUTTON,		       /* flags */
};

#ifdef STANDALONE_SOLVER

#include <stdarg.h>

int main(int argc, char **argv)
{
    game_params *p;
    game_state *s, *s2;
    char *id = NULL, *desc;
    const char *err;
    bool grade = false;
    int ret, diff;
    bool really_verbose = false;
    struct solver_scratch *sc;

    while (--argc > 0) {
        char *p = *++argv;
        if (!strcmp(p, "-v")) {
            really_verbose = true;
        } else if (!strcmp(p, "-g")) {
            grade = true;
        } else if (*p == '-') {
            fprintf(stderr, "%s: unrecognised option `%s'\n", argv[0], p);
            return 1;
        } else {
            id = p;
        }
    }

    if (!id) {
        fprintf(stderr, "usage: %s [-g | -v] <game_id>\n", argv[0]);
        return 1;
    }

    desc = strchr(id, ':');
    if (!desc) {
        fprintf(stderr, "%s: game id expects a colon in it\n", argv[0]);
        return 1;
    }
    *desc++ = '\0';

    p = default_params();
    decode_params(p, id);
    err = validate_desc(p, desc);
    if (err) {
        fprintf(stderr, "%s: %s\n", argv[0], err);
        return 1;
    }
    s = new_game(NULL, p, desc);
    s2 = new_game(NULL, p, desc);

    sc = new_scratch(p->w, p->h);

    /*
     * When solving an Easy puzzle, we don't want to bother the
     * user with Hard-level deductions. For this reason, we grade
     * the puzzle internally before doing anything else.
     */
    ret = -1;			       /* placate optimiser */
    for (diff = 0; diff < DIFFCOUNT; diff++) {
	ret = tents_solve(p->w, p->h, s->grid, s->numbers->numbers,
			  s2->grid, sc, diff);
	if (ret < 2)
	    break;
    }

    if (diff == DIFFCOUNT) {
	if (grade)
	    printf("Difficulty rating: too hard to solve internally\n");
	else
	    printf("Unable to find a unique solution\n");
    } else {
	if (grade) {
	    if (ret == 0)
		printf("Difficulty rating: impossible (no solution exists)\n");
	    else if (ret == 1)
		printf("Difficulty rating: %s\n", tents_diffnames[diff]);
	} else {
	    verbose = really_verbose;
	    ret = tents_solve(p->w, p->h, s->grid, s->numbers->numbers,
			      s2->grid, sc, diff);
	    if (ret == 0)
		printf("Puzzle is inconsistent\n");
	    else
		fputs(game_text_format(s2), stdout);
	}
    }

    return 0;
}

#endif

/* vim: set shiftwidth=4 tabstop=8: */
