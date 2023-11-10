# A very very LAME substitution of the sense_hat lib of Raspberry
# To be able to check out and debug some basic functionality
# of the small softwares developped for Sense Hat on a commercial PC

import random

class SenseHat :

    def __init__(self) :
        self.PixVector  :list  = [[0,0,0]] *64
        self.ANSIVector :list  = [16] *64
        self.low_light  :bool  = False
        self.gamma      :list  = []
        self._LetterFace :dict = {}
        self._LetterFace['A'] = [
            0,0,0,0,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,1,0,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,1,1,1,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0]
        self._LetterFace['B'] = [
            0,0,0,0,0,0,0,0,
            0,1,1,1,0,0,0,0,
            0,1,0,0,1,0,0,0,
            0,1,0,0,1,0,0,0,
            0,1,1,1,0,0,0,0,
            0,1,0,0,1,0,0,0,
            0,1,0,0,1,0,0,0,
            0,1,1,1,0,0,0,0]
        self._LetterFace['C'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,1,1,0,0,0]
        self._LetterFace['D'] = [
            0,0,0,0,0,0,0,0,
            0,1,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,1,1,1,0,0,0]
        self._LetterFace['E'] = [
            0,0,0,0,0,0,0,0,
            0,1,1,1,1,1,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,1,1,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,1,1,1,1,0,0]
        self._LetterFace['F'] = [
            0,0,0,0,0,0,0,0,
            0,1,1,1,1,1,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,1,1,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0]
        self._LetterFace['G'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,1,1,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,1,1,0,0,0]
        self._LetterFace['H'] = [
            0,0,0,0,0,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,1,1,1,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0]
        self._LetterFace['I'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,1,1,1,0,0,0]
        self._LetterFace['J'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,1,1,1,0,0,
            0,0,0,0,0,1,0,0,
            0,0,0,0,0,1,0,0,
            0,0,0,0,0,1,0,0,
            0,0,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,1,1,0,0,0]
        self._LetterFace['K'] = [
            0,0,0,0,0,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,1,0,0,0,
            0,1,0,1,0,0,0,0,
            0,1,1,0,0,0,0,0,
            0,1,0,1,0,0,0,0,
            0,1,0,0,1,0,0,0,
            0,1,0,0,0,1,0,0]
        self._LetterFace['L'] = [
            0,0,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,1,1,1,1,0,0]
        self._LetterFace['M'] = [
            0,0,0,0,0,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,1,0,1,1,0,0,
            0,1,0,1,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0]
        self._LetterFace['N'] = [
            0,0,0,0,0,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,1,0,0,1,0,0,
            0,1,0,1,0,1,0,0,
            0,1,0,0,1,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0]
        self._LetterFace['O'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,1,1,0,0,0]
        self._LetterFace['P'] = [
            0,0,0,0,0,0,0,0,
            0,1,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,1,1,1,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0]
        self._LetterFace['Q'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,1,0,1,0,0,
            0,1,0,0,1,1,0,0,
            0,0,1,1,1,1,0,0]
        self._LetterFace['R'] = [
            0,0,0,0,0,0,0,0,
            0,1,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,1,1,1,0,0,0,
            0,1,0,1,0,0,0,0,
            0,1,0,0,1,0,0,0,
            0,1,0,0,0,1,0,0]
        self._LetterFace['S'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,
            0,0,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,1,1,0,0,0]
        self._LetterFace['T'] = [
            0,0,0,0,0,0,0,0,
            0,1,1,1,1,1,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0]
        self._LetterFace['U'] = [
            0,0,0,0,0,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,1,1,0,0,0]
        self._LetterFace['V'] = [
            0,0,0,0,0,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,0,1,0,0,0,
            0,0,1,0,1,0,0,0,
            0,0,0,1,0,0,0,0]
        self._LetterFace['W'] = [
            0,0,0,0,0,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,1,0,1,0,0,
            0,1,1,0,1,1,0,0,
            0,1,0,0,0,1,0,0]
        self._LetterFace['X'] = [
            0,0,0,0,0,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,0,1,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,1,0,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0]
        self._LetterFace['Y'] = [
            0,0,0,0,0,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,0,1,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0]
        self._LetterFace['Z'] = [
            0,0,0,0,0,0,0,0,
            0,1,1,1,1,1,0,0,
            0,0,0,0,0,1,0,0,
            0,0,0,0,1,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,1,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,1,1,1,1,0,0]
        self._LetterFace['0'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,1,1,0,0,
            0,1,0,1,0,1,0,0,
            0,1,1,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,1,1,0,0,0]
        self._LetterFace['1'] = [
            0,0,0,0,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,1,1,0,0,0,0,
            0,1,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,1,1,1,1,1,0,0]
        self._LetterFace['2'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,0,0,0,0,1,0,0,
            0,0,0,0,1,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,1,0,0,0,0,0,
            0,1,1,1,1,1,0,0]
        self._LetterFace['3'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,0,0,0,0,1,0,0,
            0,0,0,1,1,0,0,0,
            0,0,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,1,1,0,0,0]
        self._LetterFace['4'] = [
            0,0,0,0,0,0,0,0,
            0,0,0,0,1,0,0,0,
            0,0,0,1,1,0,0,0,
            0,0,1,0,1,0,0,0,
            0,1,0,0,1,0,0,0,
            0,1,1,1,1,1,0,0,
            0,0,0,0,1,0,0,0,
            0,0,0,1,1,1,0,0]
        self._LetterFace['5'] = [
            0,0,0,0,0,0,0,0,
            0,1,1,1,1,1,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,1,1,1,0,0,0,
            0,0,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,1,1,0,0,0]
        self._LetterFace['6'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,0,0,0,
            0,1,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,1,1,0,0,0]
        self._LetterFace['7'] = [
            0,0,0,0,0,0,0,0,
            0,1,1,1,1,1,0,0,
            0,0,0,0,0,1,0,0,
            0,0,0,0,1,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,1,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0]
        self._LetterFace['8'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,1,1,0,0,0]
        self._LetterFace['9'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,1,1,1,0,0,
            0,0,0,0,0,1,0,0,
            0,1,0,0,0,1,0,0,
            0,0,1,1,1,0,0,0]
        self._LetterFace['.'] = [
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,1,1,0,0,0,
            0,0,0,1,1,0,0,0]
        self._LetterFace[','] = [
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,1,1,0,0,0,
            0,0,1,1,0,0,0,0]
        self._LetterFace[';'] = [
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,1,1,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,1,1,0,0,0,
            0,0,1,1,0,0,0,0]
        self._LetterFace['!'] = [
            0,0,0,0,0,0,0,0,
            0,0,0,1,1,0,0,0,
            0,0,0,1,1,0,0,0,
            0,0,0,1,1,0,0,0,
            0,0,0,1,1,0,0,0,
            0,0,0,1,1,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,1,1,0,0,0]
        self._LetterFace['?'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,
            0,1,0,0,0,1,0,0,
            0,0,0,0,0,1,0,0,
            0,0,0,0,1,0,0,0,
            0,0,0,1,1,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,1,1,0,0,0]
        self._LetterFace['+'] = [
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,1,1,1,1,1,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,0,0,0,0,0]
        self._LetterFace['-'] = [
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,0,0,0,0,0]
        self._LetterFace['/'] = [
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,1,0,0,
            0,0,0,0,0,1,0,0,
            0,0,0,0,1,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,1,0,0,0,0,0,
            0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0]
        self._LetterFace['('] = [
            0,0,0,0,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,1,0,0,0,0,0,
            0,0,1,0,0,0,0,0,
            0,0,1,0,0,0,0,0,
            0,0,1,0,0,0,0,0,
            0,0,1,0,0,0,0,0,
            0,0,0,1,0,0,0,0]
        self._LetterFace[')'] = [
            0,0,0,0,0,0,0,0,
            0,0,1,0,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,1,0,0,0,0,0]
        self._LetterFace['"'] = [
            0,0,0,0,0,0,0,0,
            0,1,1,0,1,1,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0]
        self._LetterFace[' '] = [
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0]
        self._LetterFace['%'] = [
            0,0,0,0,0,0,0,0,
            0,1,1,0,0,1,0,0,
            0,1,1,0,0,1,0,0,
            0,0,0,0,1,0,0,0,
            0,0,0,1,0,0,0,0,
            0,0,1,0,0,0,0,0,
            0,1,0,0,1,1,0,0,
            0,1,0,0,1,1,0,0]


    def _dumpScreen(self, erase_screen :bool =True) -> None :
        print("\x1b[0;38;5;16m",end="")
        if erase_screen : print("\x1b[2J\x1b[H",end="")
        PrevANSI :int = 16
        for _j in range(8) :
            for _i in range(8) :
                if self.ANSIVector[8*_j+_i] != PrevANSI :
                    PrevANSI = self.ANSIVector[8*_j+_i]
                    print(f"\x1b[1;38;5;{PrevANSI}m",end="")
                print("#",end="")
            print(f"\x1b[1;38;5;16m\n\x1b[1;38;5;{PrevANSI}m",end="")
        print("\x1b[0m")

    def _convertColors(self, _from :int =0, _to :int =64) -> None :
        for _x in range(_from,_to) :
            _R, _G, _B = self.PixVector[_x]
            _R1 = int(_R/37) ; _G1 = int(_G/37) ; _B1 = int(_B/37)
            self.ANSIVector[_x] = 36*_R1 + 6*_G1 + _B1 + 16


    def set_pixels(self, pixel_list :list) -> None :
        if len(pixel_list) != 64 : return
        self.PixVector = pixel_list
        self._convertColors()
        self._dumpScreen()

    def get_pixels(self) -> list :
        return self.PixVector

    def set_pixel(self, x :int, y :int, pixel :list) -> None :
        if len(pixel) != 3 : return
        if x not in range(8) or y not in range(8) : return
        _idx :int = 8 * y + x
        self.PixVector[_idx] = pixel
        self._convertColors(_idx,_idx+1)
        self._dumpScreen()
#    def set_pixel(self, x :int, y :int, r :int, g :int, b :int) -> None :
#        if r not in range(256) or g not in range(256) or b not in range(256) : return
#        if x not in range(8) or y not in range(8) : return
#        _idx :int = 8 * y + x
#        self.PixVector[_idx] = list((r, g, b))
#        self._convertColors(_idx,_idx+1)
#        self._dumpScreen()

    def get_pixel(self, x :int, y :int) -> list :
        if x not in range(8) or y not in range(8) : return []
        return self.PixVector[8 * y + x]

    def clear(self, colour :list =[0,0,0]) -> None :
        self.PixVector = [colour] *64
        self._convertColors()
        self._dumpScreen()
#    def clear(self, r :int, g :int, b :int) -> None :
#        self.PixVector = [list((r,g,b))] *64
#        self._convertColors()
#        self._dumpScreen()

    def get_humidity(self) -> float :
        return 40.0 + 0.1 * random.randint(0,200)
    def get_temperature(self) -> float :
        return 18.0 + 0.1 * random.randint(0,60)
    def get_temperature_from_humidity(self) -> float :
        return self.get_temperature()
    def get_temperature_from_pressure(self) -> float :
        return self.get_temperature()
    def get_pressure(self) -> float :
        return 990.0 + 0.1 * random.randint(0,200)

    def get_orientation_radians(self) -> dict :
        _ret :dict = {'pitch':0.00, 'roll':0.00, 'yaw':0.00}
        for i in ['roll', 'pitch', 'yaw'] :
            _ret[i] = 0.01 * random.randint(0,628) - 3.14
        return _ret
    def get_orientation_degrees(self) -> dict :
        _ret :dict = {'pitch':0, 'roll':0, 'yaw':0}
        for i in ['roll', 'pitch', 'yaw'] :
            _ret[i] = random.randint(0,180) - 90
        return _ret
    def get_orientation(self) -> dict :
        return self.get_orientation_degrees()

    def get_compass(self) -> float :
        return 0.1*random.randint(0,3599)
    def get_compass_raw(self) -> dict :
        _ret :dict = {'x':0.0, 'y':0.0, 'z':0.0}
        for i in ['x', 'y', 'z'] :
            _ret[i] = 0.01 * random.randint(0,100)
        return _ret

    def get_gyroscope(self) -> dict :
        return self.get_orientation_degrees()
    def get_gyroscope_raw(self) -> dict :
        return self.get_compass_raw()

    def get_accelerometer(self) -> dict :
        return self.get_orientation_degrees()
    def get_accelerometer_raw(self) -> dict :
        return self.get_compass_raw()


    def show_letter(self, s :str ="", text_colour :list =[255,255,255], back_colour :list =[0,0,0], erase_screen :bool =True) -> None:
        if s not in self._LetterFace.keys() : s = '?'
        for i in range(64) :
            self.PixVector[i] = text_colour if self._LetterFace[s][i] else back_colour
        self._convertColors()
        self._dumpScreen(erase_screen)

    def show_message(self, text_string :str ="", scroll_speed :float =1.0, text_colour :list =[255,255,255], back_colour :list =[0,0,0]) -> None:
        for s in text_string : self.show_letter(s.upper(), text_colour=text_colour, back_colour=back_colour, erase_screen=False)


    ######### NOT YET IMPLEMENTED METHODS ##############

    def set_rotation(self, r :int, redraw :bool) -> None :
        if r not in [0, 90, 180, 270] : return
        pass

    def flip_h(self, redraw :bool) -> None :
        pass
    def flip_v(self, redraw :bool) -> None :
        pass

    def load_image(self, file_path :str, redraw :bool) -> None :
        pass

    def gamma_reset(self) -> None :
        pass

    def set_imu_config(self, compass_enabled :bool =False, gyro_enabled :bool =False, accel_enabled :bool =False) -> None :
        pass



# TODO:
#    stick ??????
