#!/usr/bin/python3
#
# Timer for MK Makerspace welding area
# (c) Chris Taylor, July 2018
#

mp3file = '/home/pi/Sounds/brand.mp3'
mp3start = '/home/pi/Sounds/started.mp3'
mp3stop = '/home/pi/Sounds/stopped.mp3'
gpio_pin = 21
set_time = 1800 # 1800 seconds = 30 minutes

import tkinter as tk
import os
import subprocess
import time
import RPi.GPIO as GPIO
from mutagen.mp3 import MP3
audio = MP3(mp3file)
 
playing = False
running = False
t = set_time

root = tk.Tk()
root.attributes("-fullscreen", True)
root.wm_attributes("-topmost", 1)
root.bind("<Escape>", lambda event:root.destroy()) # keyboard escape

clock = tk.Label(root, font=('piboto', 256, 'bold'))
clock.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def play(): # begin playing alert sound and return finish time
    subprocess.Popen(['mpg123', '-q', mp3file])
    return time.time() + audio.info.length

def button_push(chan): # detect button push and take appropriate action
    global t, playing, running
    if playing:
        subprocess.call(['killall', 'mpg123'])
        playing = False
        running = False
    elif running:
        running = False
        subprocess.Popen(['mpg123', '-q', mp3stop])
    else:   
        running = True
        subprocess.Popen(['mpg123', '-q', mp3start])
    t = set_time    

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(gpio_pin, GPIO.FALLING, callback=button_push, bouncetime=500)

def count(): # count down and play alert when timer reaches zero
    global t, playing, running, endTime
    mins, secs = divmod(t, 60)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    clock.config(text=timeformat) # update time display
    if running:
        t -= 1
        if (t == 0): # timer has run out so play alert
            playing = True
            running = False
            endTime = play()
    if (playing and time.time() > endTime): # alert finished so restart
        endTime = play()
    clock.after(1000, count) # recurse after 1 second
 
count()
root.mainloop()
