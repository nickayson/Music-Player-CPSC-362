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

class Home:
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
        Description = """Creating a user friendly software that allows users to play music easily in any environment.\nThe main purpose of this software is to play music from local files with many features, \nviewing a queue of songs, a library to list all of the songs and folders, and many more."""
        self.Home = tk.Label(self.HomeWindow, bg = 'black', fg = 'white', font=("Gotham Medium typeface",16,"bold"), text=Description)
        self.Home.config(width=100,height=10)
        self.Home.grid(row=0, column=0, padx=10)
  
        self.Home.insert(tk.END, Description)

