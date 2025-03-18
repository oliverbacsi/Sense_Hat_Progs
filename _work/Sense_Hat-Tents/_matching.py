
class Scratch :

    def __init__(self) :
        # Current contents of the in-progress matching. LtoR is an array
        # of nl integers, each of which holds a value in {0,1,...,nr-1},
        # or -1 for no current assignment. RtoL is exactly the reverse.
        # Invariant: LtoR[i] is non-empty and equal to j if and only if
        # RtoL[j] is non-empty and equal to i.
        self.LtoR :list = []
        self.RtoL :list = []

        # Arrays of nl and nr integer respectively, giving the layer
        # assigned to each integer in the breadth-first search step of
        # the algorithm.
        self.Llayer :list = []
        self.Rlayer :list = []

        # Arrays of nl and nr integers respectively, used to hold the
        # to-do queues in the breadth-first search.
        self.Lqueue :list = []
        self.Rqueue :list = []

        # An augmenting path of vertices, alternating between L vertices
        # (in the even-numbered positions, starting at 0) and R (in the
        # odd positions). Must be long enough to hold any such path that
        # never repeats a vertex, i.e. must be at least 2*min(nl,nr) in size.
        self.augpath :list = []

        # Track the progress of the depth-first search at each
        # even-numbered layer. Has one element for each even-numbered
        # position in augpath.
        self.dfsstate :list = []

        # Store a random permutation of the L vertex indices,
        # if we're randomising the dfs phase.
        self.Lorder :list = []



def matching_with_scratch(s, nl :int, nr :int, adjlists, adjsizes, rs, outl :list, outr :list) -> int :
    L :int
    R :int
    i :int
    j :int
    Lqs :int
    Rqs :int
    layer :int
    target_layer :int
    found_free_R_vertex :bool

    nmin :int = min(nl,nr)
    # Oliver : There was a GOTO in the original code. To avoid this,
    # a boolean value "NotDone" is used to monitor whether the GOTO
    # should have been invoked, so the rest of the code is not executed
    # until the point where there was the target of the GOTO label originally.
    NotDone :bool =True

    # Set up the initial matching, which is empty.
    s.LtoR = [-1] * nl
    s.RtoL = [-1] * nr

    while NotDone :
        # Breadth-first search starting from the unassigned left
        # vertices, traversing edges from left to right only if they
        # are _not_ part of the matching, and from right to left only
        # if they _are_. We assign a 'layer number' to all vertices
        # visited by this search, with the starting vertices being
        # layer 0 and every successor of a layer-n node being layer n+1.
        s.Llayer = [-1] * nl
        s.Rlayer = [-1] * nr
        Lqs = 0
        for L in range(nl) :
            if s.LtoR[L] == -1 :
                s.Llayer[L] = 0
                s.Lqueue[Lqs] = L
                Lqs += 1

        layer = 0
        while NotDone :
            found_free_R_vertex = False
            Rqs = 0
            for i in range(Lqs) :
                L = s.Lqueue[i]
                if s.Llayer[L] != layer : raise Exception("Assert failed")

                for j in range(adjsizes[L]) :
                    R = adjlists[L][j]
                    if (R != s.LtoR[L]) and (s.Rlayer[R] == -1) :
                        s.Rlayer[R] = layer+1
                        s.Rqueue[Rqs] = R
                        Rqs += 1
                        if s.RtoL[R] == -1 : found_free_R_vertex = True
            layer += 1

            if found_free_R_vertex : break

            if Rqs == 0 : NotDone = False

            if NotDone :
                Lqs = 0
                for j in range(Rqs) :
                    R = s.Rqueue[j]
                    if s.Rlayer[R] != layer : raise Exception("Assert failed")
                    L = s.RtoL[R]
                    if (L != -1) and (s.Llayer[L] == -1) :
                        s.Llayer[L] = layer+1
                        s.Lqueue[Lqs] = L
                        Lqs += 1
                layer+=1
                if Lqs == 0 : NotDone = False

        # Let the "GOTO" work and if the "GOTO done" is in effect,
        # skip the remaining part of the cycle
        if not NotDone : break

        target_layer = layer
        # Vertices in the target layer are only interesting if
        # they're actually unassigned. Blanking out the others here
        # will save us a special case in the dfs loop below.
        for R in range(nr) :
            if (s.Rlayer[R] == target_layer) and (s.RtoL[R] != -1) : s.Rlayer[R] = -1

        # Choose an ordering in which to try the L vertices at the
        # start of the next pass.
        for L in range(nl) : s.Lorder[L] = L
        if rs : shuffle(s.Lorder, nl, size(s.Lorder), rs) ; #%%% This shuffle might be undefined, and size might not be needed

        # Now depth-first search through that layered set of vertices
        # to find as many (vertex-)disjoint augmenting paths as we
        # can, and for each one we find, augment the matching.

        s.dfsstate[0] = 0
        i = 0
        while True :
            # Find the next vertex to go on the end of augpath.
            if i == 0 :
                # In this special case, we're just looking for L
                # vertices that are not yet assigned.
                if s.dfsstate[i] == nl : break ; # entire DFS has finished
                L = s.Lorder[s.dfsstate[i]] ; s.dfsstate[i] += 1

                if s.Llayer[L] != 2*i : continue ; # skip this vertex
            else :
                # In the more usual case, we're going through the
                # adjacency list for the previous L vertex.
                L = s.augpath[2*i-2]
                j = s.dfsstate[i] ; s.dfsstate[i] +=1
                if j == adjsizes[L] :
                    # Run out of neighbours of the previous vertex.
                    i -= 1
                    continue

                if rs and (adjsizes[L] -j > 1) :
                    which = j + random_upto(rs, adjsizes[L] - j) ; #%%% OK, this function might need to be defined or substituted by a random.___() function call.
                    tmp = adjlists[L][which]
                    adjlists[L][which] = adjlists[L][j]
                    adjlists[L][j] = tmp
                R = adjlists[L][j]

                if s.Rlayer[R] != 2*i-1 : continue ; # skip this vertex

                s.augpath[2*i-1] = R
                s.Rlayer[R] = -1 ; # mark vertex as visited

                if 2*i-1 == target_layer :
                    # We've found an augmenting path, in the form of
                    # an even-sized list of vertices alternating
                    # L,R,...,L,R, with the initial L and final R
                    # vertex free and otherwise each R currently
                    # connected to the next L. Adjust so that each L
                    # connects to the next R, increasing the edge
                    # count in the matching by 1.
                    for j in range(0,2*i,2) :
                        s.LtoR[s.augpath[j]] = s.augpath[j+1]
                        s.RtoL[s.augpath[j+1]] = s.augpath[j]

                    # Having dealt with that path, and already marked
                    # all its vertices as visited, rewind right to
                    # the start and resume our DFS from a new
                    # starting L-vertex.
                    i = 0
                    continue

                L = s.RtoL[R]
                if s.Llayer[L] != 2*i : continue ; # skip this vertex

            s.augpath[2*i] = L
            s.Llayer[L] = -1 ; # mark vertex as visited
            i += 1
            s.dfsstate[i] = 0

    ### LABEL "done:" in the C Code was here

    # Fill in the output arrays.
    #%%% Oliver : Might be the "if outl" is not even needed, but need to be filled with empty data in advance
    if outl :
        for i in range(nl) : outl[i] = s.LtoR[i]
    if outr :
        for j in range(nr) : outr[j] = s.RtoL[j]

    # Return the number of matching edges.
    for i in range(nl) :
        if s.LtoR[i] != -1 : j += 1
    return j


def matching(nl :int, nr :int, adjlists, adjsizes, random_state, outl :list, outr :list) -> int :
    scratch = Scratch()
    return matching_with_scratch(scratch, nl, nr, adjlists, adjsizes, rs, outl, outr)
