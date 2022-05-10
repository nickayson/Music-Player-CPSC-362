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

import webbrowser

from main import *

class Home:
    # Define a callback function
    def callback(self, url):
        webbrowser.open_new_tab(url)
    
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
        Description = """C.R.I.N.G.E Creative Reading Interface Not Gaming Interface\nCreating a user friendly software that allows users to play music easily in any environment.\nThe main purpose of this software is to play music from local files with many features, \nviewing a queue of songs, a library to list all of the songs and folders, and many more."""
        self.Home = tk.Label(self.HomeWindow, bg = 'black', fg = 'white', font=("Gotham Medium typeface",16,"bold"), text=Description)
        self.Home.config(width=100,height=10)
        self.Home.grid(row=0, column=0, padx=10)
        
        #Create a Label to display the link
        self.link = tk.Label(self.HomeWindow, text="FREE MUSIC DOWNLOAD? Click Here",bg = 'black', fg = 'white',font=('Helveticabold', 10), cursor="hand2")
        self.link.grid(row=1, column=0, padx=5)
        self.link.bind("<Button-1>", lambda e: self.callback("https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"))
  
        self.Home.insert(tk.END, Description)

