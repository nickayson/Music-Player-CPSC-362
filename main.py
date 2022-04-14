# pip install pygame

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

from player import Player
from player import *

#region Main
# ----------------------------- Main -------------------------------------------
# Dimensions of app
width= root.winfo_screenwidth() 
height= root.winfo_screenheight()

root.geometry("%dx%d" % (width, height))

# Title on top right of app window
root.wm_title('CRINGE')

root['bg'] = 'black'

app = Player(master=root)
app['bg'] = 'black'
app.mainloop()
#endregion

