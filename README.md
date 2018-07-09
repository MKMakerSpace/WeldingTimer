# Welding-timer
Safety timer for welding area

This program is designed to run on a Raspberry Pi SBC

Required software installs:

  sudo apt install mpg123
  
  sudo pip3 install mutagen
  
A control button should be connected between GPIO 21 and ground (2 GPIO pins closest to USB sockets)

An audio amplifier should be plugged into the 3.5mm jack

Suitable mp3 files should be present in a "Sounds" directory in /home/pi:

  mp3file - an alarm file to be triggered after the specified elapsed time
  
  mp3start - a "countdown start" file
  
  mp3stop - a "countdown stop/reset" file
  
  
