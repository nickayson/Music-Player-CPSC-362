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

class Library:

    def openLibraryWindow(self):

        #Display Playslists by searching through file explorer Directory
        self.LibraryWindow = Toplevel(root)
        self.LibraryWindow.title("Library")
        width= root.winfo_screenwidth() 
        height= root.winfo_screenheight()
        self.LibraryWindow.geometry("%dx%d" % (width, height))
        
        self.LibraryWindow['bg'] = 'black'

		#Load button
        self.loadSongs = ttk.Button(self.LibraryWindow, style = 'TButton')
        self.loadSongs['text'] = 'Load Songs'
        self.loadSongs['command'] = self.searchfiles
        self.loadSongs.grid(row=0, column=0, pady=1)
  
        label5 = tk.Label(self.LibraryWindow, bg = 'black', fg = 'white', font=("Gotham Medium typeface",16,"bold"), text='Library')
        self.tracklist = ttk.LabelFrame(self.LibraryWindow, labelwidget=label5)
		# self.tracklist.config(width=1200,height=600)
        self.tracklist.grid(row=5, column=0, rowspan=3, pady=5)
		
		# scroll bar w
        self.scrollbar = ttk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=5, rowspan=5, sticky='ns')

		#ListBox
        self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set,
                         bg = 'black', fg = 'white')
        self.enumerate_songs()
        self.list.config(width=200,height=35)
        self.list.bind('<Double-1>', self.play_song) 

        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)

        self.reload_songs()

        #pauses music when window is closed
        def on_closing():
            self.pause_song()
            self.LibraryWindow.destroy()

        self.LibraryWindow.protocol("WM_DELETE_WINDOW", on_closing)
        self.LibraryWindow.mainloop()
