#!/usr/bin/env python3
###################################################
# Paint Drips 2 - Object oriented


#################### INIT PART ####################

from random import randint as r
from time import sleep
try :
    from sense_hat import SenseHat
except :
    try :
        from sense_emu import SenseHat
    except :
        from _sense_hat_ANSI import SenseHat


# Fade out coefficient
FadeOutCoeff :float =0.95
# Delay time between each cycle
CycleDelay :float =0.25
# Drip randomly at every n'th cycle
DripRarely :int =3
# Inherit Neighbour's value by this ratio
InheritNeighbour :float =0.4

p :list =list(())


#################### CLASS PART ####################


class PIX :

    def __init__(self, posX :int, posY :int) :
        self.R :dict =dict(())
        self.G :dict =dict(())
        self.B :dict =dict(())
        self.X :int =posX
        self.Y :int =posY
        self.Neigh :dict = dict(())
        for xx in ["U","D","L","R"] : self.Neigh[xx] = None
        for xx in range(4) :
            self.R[str(xx)] = 0
            self.G[str(xx)] = 0
            self.B[str(xx)] = 0

    def fade(self) :
        global FadeOutCoeff
        for xx in range(4) :
            self.R[str(xx)] = round(self.R[str(xx)] * FadeOutCoeff)
            self.G[str(xx)] = round(self.G[str(xx)] * FadeOutCoeff)
            self.B[str(xx)] = round(self.B[str(xx)] * FadeOutCoeff)
        self.drawMyself()

    def drip(self) :
        C = getNiceCol()
        for xx in range(4) :
            self.R[str(xx)] = C[0]
            self.G[str(xx)] = C[1]
            self.B[str(xx)] = C[2]
        self.drawMyself()
        for xx in ["U","D","L","R"] :
            if self.Neigh[xx] :
                self.Neigh[xx].receive(C,xx)

    def receive(self, _col :list, _dir :str) :
        global InheritNeighbour
        de_coo :list = {"U":[[0,1],[1,1]], "D":[[0,0],[1,0]], "L":[[1,0],[1,1]], "R":[[0,0],[0,1]]}[_dir]
        de_idx :list = {"U":["2","3"], "D":["0","1"], "L":["1","3"], "R":["0","2"]}[_dir]
        for ii in range(2) :
            dx,dy = de_coo[ii]
            pxidx = de_idx[ii]
            self.R[pxidx] = clamp( self.R[pxidx] + round(InheritNeighbour*_col[0]) )
            self.G[pxidx] = clamp( self.G[pxidx] + round(InheritNeighbour*_col[1]) )
            self.B[pxidx] = clamp( self.B[pxidx] + round(InheritNeighbour*_col[2]) )
        self.drawMyself()

    def drawMyself(self) :
        for dy in range(2) :
            for dx in range(2) :
                pxidx = str(2*dy+dx)
                s.set_pixel(self.X*2+dx, self.Y*2+dy, self.R[pxidx], self.G[pxidx], self.B[pxidx])


#################### PROC PART ####################


def getNiceCol() -> list :
    ret :list = list(())
    L=r(200,255) ; ret=list((L,L,L))
    p=r(0,2) ; q=p
    while q == p : q = r(0,2)
    ret[q]=round(L/6.0) ; ret[p]=round(L/2.0)
    return ret

def clamp(_val :int) -> int :
    return max(min(_val,255),0)


#################### MAIN PART ####################


s=SenseHat()
s.clear()

for j in range(4) :
    for i in range(4) :
        p.append(PIX(i,j))

for j in range(4) :
    for i in range(4) :
        if j-1 in range(4) : p[4*j+i].Neigh["U"] = p[4*(j-1)+i]
        if j+1 in range(4) : p[4*j+i].Neigh["D"] = p[4*(j+1)+i]
        if i-1 in range(4) : p[4*j+i].Neigh["L"] = p[4*j+(i-1)]
        if i+1 in range(4) : p[4*j+i].Neigh["R"] = p[4*j+(i+1)]


while True :
    for e in p : e.fade()
    if not r(0,DripRarely) : p[r(0,15)].drip()
    sleep(CycleDelay)

