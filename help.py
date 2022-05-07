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

class Help:
    def openHelpWindow(self):
         # Instructions for each button and how to navigate around the app
        self.HelpWindow = Toplevel(root)
        self.HelpWindow.title("Help")
        width= root.winfo_screenwidth() 
        height= root.winfo_screenheight()
        self.HelpWindow.geometry("%dx%d" % (width, height))
        self.HelpWindow['bg'] = 'black'
		
		# These values help calculate the correct font size for the screen so that all text will be displayed
        w_h_ratio = (width / height) * 10000
        text_length = 0
        font_size = 0
		# two options: define x here as 3.348 or wait until after mute button info to calculate
		# Used to adjust ratio for text size
        x = 3.348
        font_size = 0
		# Overall title for the help page
        self.helpTitle = tk.Label(self.HelpWindow, bg = 'black', fg = 'white', font=("Gotham Medium typeface",22,"bold")
                            , text="Welcome to the Help Page" )	
		# Anchor to North point on page (top center)
        self.helpTitle.pack(anchor= 'n')

		# Mute button function info
        text_="""Mute button information:\nWhen you press the mute button, the volume level will be set to zero.\nThe volume can be unmuted by increasing the volume by interacting with\nthe volume slider or by pressing the volume up button."""
        text_length = len(text_)
        font_size = int((w_h_ratio / text_length) / x)
        self.muteInfo = tk.Label(self.HelpWindow, bg = 'blue', fg = 'white', font=("Gotham Medium typeface",font_size - 6,"bold"), text=text_) 
		# Anchor label to NW corner (top left)
        self.muteInfo.pack(anchor= 'nw')

		# Info about viewing the music library
        text_="""Library Page:\nThe library screen is a way to see all of the songs you have loaded\nfrom your device. The screen will display the name of the folder you have\nselected as well as the music files that are in that folder. You can\nalso click on a song on the list to play it. There is also a load\nsong button on the screen so you can load more songs."""
        text_length = len(text_)
        font_size = int((w_h_ratio / text_length) / x)
        self.LibraryInfo = tk.Label(self.HelpWindow, bg = 'purple', fg = 'white', font=("Gotham Medium typeface",font_size + 2,"bold"), text=text_)
		# Anchor just below above Label
        self.LibraryInfo.pack(anchor='ne', pady= 10)

		# Info for how to load songs
        text_= """Loading Songs:\nYou can easily add songs from your computer by uploading them as files.\nSimply click on the "Load Song" button to bring up a window from which you\ncan navigate through your files to find songs to upload. Once a song has\nbeen uploaded, it will appear in your library. There are additional 'Load\nSong' buttons on the Queue and Library Pages."""
        text_length = len(text_)
        font_size = int((w_h_ratio / text_length) / x)
        self.about_loadsong = tk.Label(self.HelpWindow, bg = '#4AC1E1', fg = 'white', font=("Gotham Medium typeface",font_size + 3,"bold"), text= text_)	
		# Anchor label to West point (middle left)
        self.about_loadsong.pack(anchor= 'w', pady= 1)

		# Information about the Queue
        text_= """Queue Information:\nYou can view your current queue by pressing the queue button on the\nhomepage. This will bring up a new window that will show what songs\nare next to be played and in what order they will be played. You can play\nsongs from this window as well by clicking on them."""
        text_length = len(text_)
        font_size = int((w_h_ratio / text_length) / x)
        self.queueInfo = tk.Label(self.HelpWindow, bg= 'green', fg = 'white', font=("Gotham Medium typeface",font_size - 2,"bold"), text= text_)
		# Anchor label to E corner (middle right)
        self.queueInfo.pack(anchor= 'e', pady= 10)

        # Created a class instance so we can call the openMoreHelp function from this class
        h = Help()
        # Button to open the additional help window
        self.moreHelp = tk.Button(self.HelpWindow, bg='#FF0000', fg= 'white', font=("Gotham Medium typeface", 14, "bold"))
        self.moreHelp['text'] = 'For more help,\nclick here'
        self.moreHelp['command'] = h.openMoreHelp
        self.moreHelp.pack(anchor='center', pady= 10)

	# More help window where we can have a labeled image of what each button does
    def openMoreHelp(self):
        self.moreHelpWindow = Toplevel(root)
        self.moreHelpWindow.title("More Help")
        width= root.winfo_screenwidth() 
        height= root.winfo_screenheight()
        self.moreHelpWindow.geometry("%dx%d" % (width, height))

        self.moreHelpWindow['bg'] = 'black'
        # Puts a label containing an image with more descriptions of what buttons do
        self.descriptions = tk.Label(self.moreHelpWindow, image=moreHelp)
        self.descriptions.pack(anchor='center')

        