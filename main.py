# pip install pygame
# pip install mutagen
# pyinstaller --onefile -w player.py

import os
import pickle
import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer

#region Main
# ----------------------------- Main -------------------------------------------
root = tk.Tk()

# Dimensions of app
width= root.winfo_screenwidth() 
height= root.winfo_screenheight()

#root bottom of player
root.geometry("%dx%d" % (width, height))

# Title on top right of app window
root.wm_title('CRINGE')

root['bg'] = 'black'

sound = PhotoImage(file='images/sounds.gif')
img = PhotoImage(file='images/Logo.gif')
next_ = PhotoImage(file = 'images/next.gif')
prev = PhotoImage(file='images/previous.gif')
play = PhotoImage(file='images/play.gif')
pause = PhotoImage(file='images/pause.gif')
loadsongs = PhotoImage(file= 'images/loadsongs.png')
moreHelp = PhotoImage(file='images/moreHelp.png')

#endregion

