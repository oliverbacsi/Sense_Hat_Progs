#!/usr/bin/env python3
##########################################################
# Space Weather monitoring
#
# Monitors space weather activity & geomagnetic storms.
# Data collected from NOAA.
# Inspired by the wmspaceweather dock app of WindowMaker.
#

import re, time, urllib.request
try :
    from sense_hat import SenseHat
except :
    try :
        from sense_emu import SenseHat
    except :
        from _sense_hat_ANSI import SenseHat


# Set this to the download interval in seconds. Default=900 (15 mins)
DOWNLOADINTERVAL :int = 900

# Color scheme. You can change the palette by finetuning this:
COLOR :dict = {'red':[220,0,0], 'orange':[200,100,0], 'yellow':[180,180,0], 'green':[0,220,0], 'blue':[0,80,220], 'B':[0,220,0], 'C':[180,180,0], 'M':[200,100,0], 'X':[220,0,0], 'KpBG':[0,0,48], 'BlBG':[0,0,48], 'XRBG':[0,0,48]}



#################### CLASS PART ####################

class SpWeather :

    def __init__(self) :
        # Proton flux > 1MeV
        self.P1 :float =0.0
        # Proton flux > 10MeV
        self.P2 :float =0.0
        # Proton flux > 100MeV
        self.P3 :float =0.0
        # Electron flux > 2MeV
        self.E1 :float =0.0
        # X-Ray letter
        self.XL :str ='B'
        # X-Ray scale
        self.XS :float =0.0
        # X-Ray value
        self.XV :float =0.0
        # Kp indices
        self.Kp :list =[0.0]*8
        # Last update
        self.LastUpdate :float =0.0
        # Counter to reload
        self.Counter = 0
        # Blinker status
        self.Blinker :bool =True
        # Could load valid data in the last download
        self.DataValid :bool =False


    def blink(self) -> None :
        """Blink the status LED in the top-right corner.
        Color is determined by the up-to-date status of the data"""

        global COLOR
        self.Blinker = not self.Blinker
        # Change color based on data status:
        # Red if could not retrieve data, orange if data is old,
        # green if 5-15mins, blue if fresh
        Age :float = time.time() - self.LastUpdate
        _col :list
        if not self.DataValid :
            _col = COLOR['red']
        elif Age > 900.0 :
            _col = COLOR['orange']
        elif Age > 300.0 :
            _col = COLOR['green']
        else :
            _col = COLOR['blue']
        if self.Blinker :
            s.set_pixel(7,0,_col)
        else :
            s.set_pixel(7,0,COLOR['BlBG'])


    def download(self) -> None :
        """Download Space Weather data from NOAA"""

        # Consider data as valid, but at the first fail invalidate it.
        self.DataValid = True
        Valid :dict = {'X':False, 'P':False, 'E':False, 'K':False}
        fh = open("_SpaceWeather-essential-data-lines-out.txt","w")

        # Load the particle flux from the current space weather indices report:
        PageContents2 = urllib.request.urlopen("https://services.swpc.noaa.gov/text/current-space-weather-indices.txt").read()
        PageData2 = str(PageContents2).split("\\n")
        # The data is in the first uncommented line after the phrase "Proton flux"
        ReadNextUncommented :bool =False
        Valid['P'] =False  ; Valid['E'] =False
        for DataLine in PageData2 :
            if re.match("^#.*",DataLine) :
                # Commented line
                if re.match(".*GOES.Proton.Flux.*",DataLine) : ReadNextUncommented =True
            else :
                # Uncommented line
                if ReadNextUncommented :
                    mPart = re.match("^\s+([0-9.e+\-]+)\s+([0-9.e+\-]+)\s+([0-9.e+\-]+)\s+([0-9.e+\-]+)\s+([0-9.e+\-]+)\s+.*",DataLine)
                    if mPart :
                        fh.write("Particle Flux:\n"+str(mPart[0])+"\n\n")
                        self.P1 = float(mPart[1])
                        self.P2 = float(mPart[2])
                        self.P3 = float(mPart[3])
                        Valid['P'] = True
                        self.E1 = float(mPart[4])
                        Valid['E'] = True
                        self.XV = float(mPart[5])
                        break

        # Load the geomagnetic data from the daily geomagnetic indices report:
        Valid['K'] =False
        PageContents1 = urllib.request.urlopen("https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt").read()
        PageData1 = str(PageContents1).split("\\n")
        # The data is in the last 2 rows with data, omitting the "-1" values
        LastRow :str =""
        PrevRow :str =""
        for DataLine in PageData1 :
            if len(DataLine.strip()) > 10 :
                PrevRow = LastRow
                LastRow = DataLine
        DataLine = PrevRow[65:] + " " + LastRow[65:]
        DataList = DataLine.split()
        fh.write(f"Kp indices:\n{PrevRow}\n{LastRow}\n\n")
        i :int =5
        while i > -1 and len(DataList) :
            self.Kp[i] = float(DataList.pop())
            if self.Kp[i] >= 0.0 : i -= 1
        if i < 0 : Valid['K'] =True
        
        # Load the X-Ray events from the solar geophysical events report:
        Valid['X'] =False
        PageContents3 = urllib.request.urlopen("https://services.swpc.noaa.gov/text/solar-geophysical-event-reports.txt").read()
        PageData3 = str(PageContents3).split("\\n")
        # The data is in the last valid data row with an X-Ray report
        ReportLine :str =""
        for DataLine in PageData3 :
            if len(DataLine) > 62 :
                if DataLine[43:46].upper() == "XRA" :
                    ReportLine = DataLine
                    self.XL = DataLine[58].upper()
                    self.XS = float(DataLine[59:62])
                    Valid['X'] =True
        # If did not manage to get X-Ray event, then it's the background X-Ray, and level is the multiplicant of 1e-06
        if not Valid['X'] :
            self.XL = 'B'
            self.XS = self.XV * 1000000.0
        fh.write(f"X-Ray event:\n{ReportLine}\n\n")

        # If anything is not valid, then let's not consider it as valid
        for _idx in ['X','P','E','K'] :
            if not Valid[_idx] : self.DataValid = False

        # If we managed to load all data, the new update can be set.
        # TODO : This means that the last update time will mean
        #        the last successful data download form the server, but
        #        this does not necessarily mean that the data is fresh.
        #        A more sophisticated method would be to check the
        #        data date inside the file and consider the
        #        age of the data accordingly!
        if self.DataValid : self.LastUpdate = time.time()
        fh.close()


    def redraw(self) -> None :
        """Redraw the screen based on the Space Weather Data"""

        global COLOR
        # Top status row: protons, electrons and status blinker
        s.set_pixel(0,0, getCol(self.P1, 31.0, 100.0, 310.0, 1000.0))
        s.set_pixel(1,0, getCol(self.P2,  0.2,   0.5,   1.5,    5.0))
        s.set_pixel(2,0, getCol(self.P3,  0.1,   0.3,   1.0,    3.0))
        s.set_pixel(3,0, [0,0,0])
        s.set_pixel(4,0, getCol(self.E1, 310000.0, 1000000.0, 3100000.0, 10000000.0))
        s.set_pixel(5,0, [0,0,0])

        # Separator column between Kp and X-Ray
        for _j in range(8) : s.set_pixel(6,_j,[0,0,0])

        # X-Ray bar on the right edge. Color based on the letter
        for _j in range(1,8) : s.set_pixel(7,_j,COLOR['XRBG'])
        for _lim,_pix in [[-1.0, 7], [1.999, 6], [3.999, 5], [5.999, 4], [6.999, 3], [7.999, 2], [8.999, 1]] :
            if self.XV > _lim : s.set_pixel(7,_pix,COLOR[self.XL])

        # The last 6 Kp bars (8 provided by NOAA, but no space on the display)
        for _i in range(6) :
            for _j in range(1,8) : s.set_pixel(_i,_j,COLOR['KpBG'])
            for _lim,_pix,_col in [[-1.0, 7, 'blue'], [1.999, 6, 'green'], [3.999, 5, 'yellow'], [5.999, 4, 'orange'], [6.999, 3, 'red'], [7.999, 2, 'red'], [8.999, 1, 'red']] :
               if self.Kp[_i+2] > _lim : s.set_pixel(_i, _pix, COLOR[_col])



    def tick(self) -> None :
        """Receive a tick each second"""

        global DOWNLOADINTERVAL
        self.blink()
        self.Counter += 1
        if self.Counter > DOWNLOADINTERVAL :
            self.Counter = 0
            self.download()
            self.redraw()
            self.blink()



#################### PROC PART ####################

def getCol(_val :float, _lim1 :float, _lim2 :float, _lim3 :float, _lim4 :float) -> list :
    """Return the LED color based on the value and limits.
    Parameters:
    :param _val : The value to evaluate as float.
    :param _lim1 : First limit between blue and green.
    :param _lim2 : Second limit between green and yellow.
    :param _lim3 : Third limit between yellow and orange.
    :param _lim4 : Fourth limit between orange and red.
    :return : RGB triplet as list"""

    global COLOR
    if _val >= _lim4 : return COLOR['red']
    if _val >= _lim3 : return COLOR['orange']
    if _val >= _lim2 : return COLOR['yellow']
    if _val >= _lim1 : return COLOR['green']
    return COLOR['blue']



#################### MAIN PART ####################

s = SenseHat()
s.clear()
sw = SpWeather()
sw.download()
sw.redraw()

while True :
    sw.tick()
    time.sleep(1)
