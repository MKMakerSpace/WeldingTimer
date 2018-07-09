#!/usr/bin/python3
#
# Timer for MK Makerspace welding area
# (c) Chris Taylor, July 2018
#

mp3file = '/home/pi/Sounds/klaxon.mp3'
mp3start = '/home/pi/Sounds/started.mp3'
mp3stop = '/home/pi/Sounds/stopped.mp3'
gpio_pin = 21

import tkinter as tk
import os
import subprocess
import time
import RPi.GPIO as GPIO
from mutagen.mp3 import MP3
audio = MP3(mp3file)

playing = False
running = False

root = tk.Tk()
root.attributes("-fullscreen", True)
root.wm_attributes("-topmost", 1)
root.bind("<Escape>", lambda event:root.destroy()) # keyboard escape

clock = tk.Label(root, font=('piboto', 256, 'bold'))
clock.grid(row = 10, column = 2, padx = 5, pady = 5)

def play():
    subprocess.Popen(['mpg123', mp3file])            
    return time.time() + audio.info.length

def reset_timer():
    global t
    t = 1800 # 1800 seconds = 30 minutes

def button_push(chan):
    global playing, running
    if playing:
        subprocess.call(['killall', 'mpg123'])
        playing = False
        running = False
    elif running:
        running = False
        subprocess.Popen(['mpg123', mp3stop])
    else:   
        running = True
        subprocess.Popen(['mpg123', mp3start])
    reset_timer()    

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(gpio_pin, GPIO.FALLING, callback=button_push, bouncetime=500)
      
reset_timer()

def count():
    global t, playing, running, endTime
    mins, secs = divmod(t, 60)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    clock.config(text=timeformat)
    if running:
        t -= 1
    if (t == 0):
        playing = True
        running = False
        endTime = play()
    if (playing and time.time() > endTime):
        endTime = play()
    clock.after(1000, count)
 
count()

root.mainloop()
