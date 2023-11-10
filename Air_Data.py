#!/usr/bin/env python3
########################################################x
# Air Data Displaying Program

# from _sense_hat_ANSI import SenseHat
from sense_hat import SenseHat
s=SenseHat()
from time import sleep

while True :
    s.show_message("T "+str(round(s.get_temperature()))+"C", text_colour=(80,80,0) )
    sleep(1)
    s.show_message("P "+str(round(s.get_pressure()))+"mb", text_colour=(0,100,0) )
    sleep(1)
    s.show_message("H "+str(round(s.get_humidity()))+"%", text_colour=(0,80,80) )
    sleep(1)
