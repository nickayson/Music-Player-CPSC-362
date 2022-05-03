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

class QPage:
    def openQueueWindow(self):
        self.QueueWindow = Toplevel(root)
        self.QueueWindow.title("Queue")
        width= root.winfo_screenwidth() 
        height= root.winfo_screenheight()
        self.QueueWindow.geometry("%dx%d" % (width, height))

        self.QueueWindow['bg'] = 'black'

		#Load button
        self.loadSongs = ttk.Button(self.QueueWindow, style = 'TButton')
        self.loadSongs['text'] = 'Load Songs'
        self.loadSongs['command'] = self.retrieve_songs
        self.loadSongs.grid(row=0, column=0, pady=1)
  
        label5 = tk.Label(self.QueueWindow, bg = 'black', fg = 'white', font=("Gotham Medium typeface",16,"bold"), text='Queue')
        self.tracklist = ttk.LabelFrame(self.QueueWindow, labelwidget=label5)
		# self.tracklist.config(width=1200,height=600)
        self.tracklist.grid(row=5, column=0, rowspan=3, pady=5)
		
		# scroll bar w
        self.scrollbar = ttk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=5, rowspan=5, sticky='ns')

		#ListBox
        self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set, selectbackground='sky blue'
                         ,bg = 'black', fg = 'white')
        self.enumerate_songs()
        self.list.config(width=200,height=35)
        self.list.bind('<Double-1>', self.play_song) 

        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)