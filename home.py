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

from main import *

class HomePage:
    def openHomeWindow(self):
        self.HomeWindow = Toplevel(root)
        self.HomeWindow.title("Home")
        width= root.winfo_screenwidth() 
        height= root.winfo_screenheight()
        self.HomeWindow.geometry("%dx%d" % (width, height))

        self.HomeWindow['bg'] = 'black'

        self.image = tk.Label(self.HomeWindow, image=img)
        self.image.configure(width=525, height=400)
        self.image.grid(row=2,column=0)
		# Create text widget and specify size.
  
        self.Home = tk.Text(self.HomeWindow, bg = 'black', fg = 'white', font=("Gotham Medium typeface",16,"bold"))	
		#Put in text description of what the software does and why we created it with the logo.png photo
        Description = """Creating a user friendly software that allows users to play music easily in any environment.\nThe main purpose of this software is to play music from local files with many features such as creating playlists,\nfavoriting a song, creating a queue, and many more."""
        self.Home.config(width=100,height=10)
        self.Home.grid(row=0, column=0, padx=10)
  
        self.Home.insert(tk.END, Description)
        # return self.HomeWindow

