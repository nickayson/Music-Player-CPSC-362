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

class LibraryPage:
    def openLibraryWindow(self):
        #Display Playslists by searching through file explorer Directory
        self.LibraryWindow = Toplevel(root)
        self.LibraryWindow.title("Library")
        width= root.winfo_screenwidth() 
        height= root.winfo_screenheight()
        self.LibraryWindow.geometry("%dx%d" % (width, height))

		# #Load button
		# self.loadSongs = ttk.Button(self.LibraryWindow, style = 'TButton')
		# self.loadSongs['text'] = 'Load Songs'
		# self.loadSongs['command'] = self.retrieve_songs
		# self.loadSongs.grid(row=0, column=0, pady=1)

		# label5 = tk.Label(self.LibraryWindow, bg = 'black', fg = 'white', font=("Gotham Medium typeface",16,"bold"), text='Your Music Library')
		# self.library = ttk.LabelFrame(self.LibraryWindow, labelwidget=label5)
		# # self.tracklist.config(width=1200,height=600)
		# self.library.grid(row=5, column=0, rowspan=3, pady=5)
		
		# # scroll bar w
		# self.scrollbar = ttk.Scrollbar(self.library, orient=tk.VERTICAL)
		# self.scrollbar.grid(row=0, column=5, rowspan=5, sticky='ns')

		# #ListBox
		# self.list = tk.Listbox(self.library, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set, selectbackground='sky blue'
        #                  ,bg = 'black', fg = 'white')
		

		## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  ##
		## Do something like a for loop to go through the number of folders we have in the music library directory? ##
		## The library directory should be the same as the filepath of an .mp3 in the queue, except just minus the  ##
		## song and playlist folder(?). I.e., if the path of a song in the queue is something like:                 ##
		## "User1/Desktop/Music_Library/Playlist1/song1.mp3", all we would have to do is go two directories up or   ##
		## erase the last two filepaths on the end to find the directory that is the music library with all of the  ##
		## folders of songs, which is what the library page wants. I think once we have the filepath of the music   ##
		## library, we just have to use a for loop to loop through the number of folders at that directory and then ##
		## use the same enumerate_songs function on each folder inside the loop. I think this could work, but I'm   ##
		## not entirely sure how to implement looping through the files at a directory given the path. Removing the ##
		## song name and folder name from the filepath shouldn't be too difficult, I'm going to work on this later  ##
		## today (5/1) and tomorrow (5/2) and then see if I can get the filepath working with help from you all.    ##
		## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  ## 
		# self.enumerate_songs()
		# self.list.config(width=200,height=35)
		# self.list.bind('<Double-1>', self.play_song) 

		# self.scrollbar.config(command=self.list.yview)
		# self.list.grid(row=0, column=0, rowspan=5)