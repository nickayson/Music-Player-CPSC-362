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

class HelpPage:
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
        text_="""Mute button information:\nOur mute button will record your volume level from before mute was\nhit; this level will be restored upon being unmuted. The volume can be\nunmuted by interacting with any of the volume control buttons or the slider."""
        text_length = len(text_)
        font_size = int((w_h_ratio / text_length) / x)
        self.muteInfo = tk.Label(self.HelpWindow, bg = 'blue', fg = 'white', font=("Gotham Medium typeface",font_size - 8,"bold"), text=text_) 
		# Anchor label to NW corner (top left)
        self.muteInfo.pack(anchor= 'nw')

		# Info about viewing the music library
        text_="""How to view your Library:\nYour music library comprises all of the songs that you have loaded into\nthe player from your device. You can view this by pressing the library\nbutton from the home screen. You can also sort your songs by different\ncriteria using the sort option(?). You can perform any normal actions\non these songs, such as adding to a playlist or the queue."""
        text_length = len(text_)
        font_size = int((w_h_ratio / text_length) / x)
        self.LibraryInfo = tk.Label(self.HelpWindow, bg = 'purple', fg = 'white', font=("Gotham Medium typeface",font_size,"bold"), text=text_)
		# Anchor just below above Label
        self.LibraryInfo.pack(anchor='ne', pady= 10)

		# Info for how to load songs
        text_= """Loading Songs:\nYou can easily add songs from your computer by uploading them as files.\nSimply click on the "Load Song" button to bring up a window from which you\ncan navigate through your files to find songs to upload. Once a song has\nbeen uploaded, it will appear in your library. There are additional 'Load\nSong' buttons on the Queue and Library Pages."""
        text_length = len(text_)
        font_size = int((w_h_ratio / text_length) / x)
        self.about_loadsong = tk.Label(self.HelpWindow, bg = '#4AC1E1', fg = 'white', font=("Gotham Medium typeface",font_size,"bold"), text= text_)	
		# Anchor label to West point (middle left)
        self.about_loadsong.pack(anchor= 'w', pady= 1)

		# Information about the Queue
        text_= """Queue Information:\nYou can view your current queue by pressing the queue button on the\nhomepage. This will bring up a new window that will show what songs\nare next to be played and in what order they will be played."""
        text_length = len(text_)
        font_size = int((w_h_ratio / text_length) / x)
        self.queueInfo = tk.Label(self.HelpWindow, bg= 'green', fg = 'white', font=("Gotham Medium typeface",font_size - 8,"bold"), text= text_)
		# Anchor label to E corner (middle right)
        self.queueInfo.pack(anchor= 'e', pady= 10)

		# Label that tells how to make playlists
        text_ = """Creating a Playlist:\nNot sure if we are implementing this button, so this is just a placeholder for now.\n\n"""
        text_length = len(text_)
        font_size = int((w_h_ratio / text_length) / x)
        self.creatingPlaylists = tk.Label(self.HelpWindow, bg= '#E00DF9', fg = 'white', font=("Gotham Medium typeface",font_size - 33,"bold"), text=text_)
        # Anchor label to E corner (middle right)
        self.creatingPlaylists.pack(anchor= 'sw', pady= 1)
		# Button to open the additional help window

        self.moreHelp = tk.Button(self.HelpWindow, bg='#FF0000', fg= 'white', font=("Gotham Medium typeface", 12, "bold"))
        self.moreHelp['text'] = 'For more help,\nclick here'
        self.moreHelp['command'] = self.openMoreHelp
        self.moreHelp.pack(anchor='center', pady= 10)

	# More help window where we can have a labeled image of what each button does
    def openMoreHelp(self):
        self.moreHelpWindow = Toplevel(root)
        self.moreHelpWindow.title("More Help")
        width= root.winfo_screenwidth() 
        height= root.winfo_screenheight()
        self.moreHelpWindow.geometry("%dx%d" % (width, height))

        self.moreHelpWindow['bg'] = 'black'

        