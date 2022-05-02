from msilib.schema import TextStyle
import os
import pickle
import tkinter as tk
import time

from tkinter import *
from tkinter import ttk
from tkinter import font
from turtle import bgcolor, color
from ttkthemes import ThemedTk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer

from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen import MutagenError

'''
THINGS TO DO:

Make Library Page 
	Have it display all of the folders with mp3 files in it
	Have it display all of the mp3 files under those folders
	Display both the folders and the individual mp3 files

Make back button to go back to previous windows (to do last)

Make Help Page
look nicer with similar formatting to the help page

Also seperate new windows into new classes and different files so it looks nicer (to do last)

'''
muted = FALSE
class Player(tk.Frame): 
    #region INIT
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		mixer.init()

		if os.path.exists('songs.pickle'):
			with open('songs.pickle', 'rb') as f:
				self.playlist = pickle.load(f)
		else:
			self.playlist=[]

		self.current = 0
		self.paused = True
		self.played = False
		self.folderpath = ""

		self.create_frames()
		self.track_widgets()
		self.control_widgets()
		self.volume_widgets()
		self.nav_widgets()
		self.progress_widgets()
  #endregion
  
    #region CREATE_FRAMES
	def create_frames(self):
    #  CREATES ALL OF THE FRAMES
		s1 = ttk.Style()
		s1.theme_use('clam')
		s1.configure(
			'TLabelframe',
			foreground = 'yellow',
			background='black'
		)
  
		s2 = ttk.Style()
		s2.theme_use('clam')
		s2.configure('TLabelframe', background = 'black', foreground = 'white')
  
		style = ttk.Style()
		style.theme_use('clam')
  
		style.configure('TButton', background = 'black', foreground = 'white', font=10, borderwidth=1, focusthickness=3, focuscolor='none')
		style.map('TButton', background=[('active','#FFF59E')])

		label1 = tk.Label(root, bg = 'black')
		self.track = ttk.LabelFrame(self, style = 'TLabelframe', labelwidget = label1)
		# self.track.config(font = "Helvetica", fontsize=12)
		self.track.config(width=1000,height=500)
		self.track.grid(row=5, column=10, padx=10)
  
		label2 = tk.Label(root, bg = 'black')
		self.controls = ttk.LabelFrame(self, labelwidget=label2)
		self.controls.config(width=1000,height=500)
		self.controls.grid(row=10, column=10, pady=5, padx=10)

		label3 = tk.Label(root, bg='black')
		self.volumew = ttk.LabelFrame(self, labelwidget=label3)
		self.volumew.config(width=800, height=1000)
		self.volumew.grid(row=5, column=15, pady=5, padx=10)

		label4 = tk.Label(root, bg='black')
		self.nav = ttk.LabelFrame(self, labelwidget=label4)
		self.nav.config(width=500,height=1000)
		self.nav.grid(row=5, column=0, pady=5, padx=10)
  
		label5 = tk.Label(root, bg='black')
		self.progress = ttk.LabelFrame(self, labelwidget=label5)
		# self.progress.config(width=500,height=500)
		self.progress.grid(row=15, column=10, padx=10)
  
		self.status_bar = tk.Label(root,text='', bg='black', fg='white',anchor=E, font=("calibri",12,"bold"))
		self.status_bar.pack(fill=X, side=BOTTOM, ipady=2)
    #endregion
	
    #region TRACK_WIDGETS
	def track_widgets(self):
    #  CHANGE THE CANVAS SIZE
		self.canvas = tk.Label(self.track, image=img)
		self.canvas.configure(width=525, height=400)
		self.canvas.grid(row=0,column=0)

		self.songtrack = tk.Label(self.track, font=("Gotham Medium typeface",16,"bold"),
						bg="#FFF59E",fg="dark blue")
		self.songtrack['text'] = 'C.R.I.N.G.E Music Player V5'
		self.songtrack.config(width=30, height=1)
		self.songtrack.grid(row=1,column=0,padx=10)
	#endregion
	
	#region CONTROL_WIDGETS
	def control_widgets(self):
		#Load button
		self.loadSongs = ttk.Button(self.controls, style = 'TButton')
		self.loadSongs['text'] = 'Load Songs'
		self.loadSongs['command'] = self.retrieve_songs
		self.loadSongs.grid(row=0, column=0, padx=10)
  
        #PREVIOUS
		self.prev = ttk.Button(self.controls, image=prev)
		self.prev['command'] = self.prev_song
		self.prev.grid(row=0, column=1)
  
		#PAUSE
		self.pause = ttk.Button(self.controls, image=pause)
		self.pause['command'] = self.pause_song
		self.pause.grid(row=0, column=2)
  
        #NEXT
		self.next = ttk.Button(self.controls, image=next_)
		self.next['command'] = self.next_song
		self.next.grid(row=0, column=3)	
	#endregion
 
	#region progress widget
	def progress_widgets(self):
		self.slider_value = tk.DoubleVar()
		self.my_slider = tk.Scale(self.progress, from_=0, to=100, orient=HORIZONTAL, length=700,
                                resolution=0.5, showvalue=True, tickinterval=30, digit=4,
                                variable=self.slider_value, bg = 'black', fg = 'white')
		self.my_slider['command'] = self.slide
		self.my_slider.grid(row=1, column=1)
	#endregion
 
	#region VOLUME_WIDGET
	def volume_widgets(self):
	    #VOLUME SLIDER
		self.volume = tk.DoubleVar(self)
		self.slider = tk.Scale(self.volumew, from_ = 10, to = 0, bg = 'black', fg = 'white' ) #from_ x = top value, to x = bottom value
		self.slider['variable'] = self.volume
		self.volume.set(5)
		mixer.music.set_volume(0.5)
		self.slider['command'] = self.change_volume
		self.slider.grid(row=1, column=5, padx=5)

		#VOLUME UP 
		self.volUp = ttk.Button(self.volumew, style = 'TButton')
		self.volUp['text'] = 'Volume Up'
		self.volUp['command'] = self.increase_volume
		self.volUp.grid(row=0, column=5, pady=10, padx=10) #ipadx is a bandaid fix to make the vol up/downs the same width, couldn't get columnspan to work

		#VOLUME DOWN 
		self.volDown = ttk.Button(self.volumew, style = 'TButton')
		self.volDown['text'] = 'Volume Down'
		self.volDown['command'] = self.decrease_volume
		self.volDown.grid(row=3, column=5, pady=10)

		#MUTE
		self.mute = ttk.Button(self.volumew, style = 'TButton')
		self.mute['text'] = 'Mute'
		self.mute['command'] = self.mute_volume   #need to create function
		self.mute.grid(row=4, column=5, pady=5)

		#VOLUME
		self.volNum = ttk.Button(self.volumew, style = 'TButton')
		self.volNum['text'] = 'Volume #' # '#' is placeholder for number input
		# self.volDown['command'] = self.set_volume   #need to create function
		self.volNum.grid(row=5, column=5, pady=5)
	#endregion

    #region RETRIEVE SONGS
	def retrieve_songs(self):
        #FILE SEARCHER
		self.songlist = []
		directory = filedialog.askdirectory()
		for root_, dirs, files in os.walk(directory):
				for file in files:
					if os.path.splitext(file)[1] == '.mp3':
						self.folderpath = root_
						global path
						path = (root_ + '/' + file).replace('\\','/')
						self.songlist.append(path)

		with open('songs.pickle', 'wb') as f:
			pickle.dump(self.songlist, f)
		self.playlist = self.songlist
		# self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
		self.list.delete(0, tk.END)
		self.enumerate_songs()
	#endregion

	#region ENUMERATE SONGS
	def enumerate_songs(self):
		for index, song in enumerate(self.playlist):
			self.list.insert(index, os.path.basename(song))
	#endregion

	#region SONG CONTROL
	def play_song(self, event=None):
		if event is not None:
			self.current = self.list.curselection()[0]
			for i in range(len(self.playlist)):
				self.list.itemconfigure(i, bg="white")
    
		print(self.playlist[self.current])
		mixer.music.load(self.playlist[self.current])
		self.songtrack['anchor'] = 'w' 
		self.songtrack['text'] = os.path.basename(self.playlist[self.current])
  
		# get song length
		self.play_time()

		self.pause['image'] = play
		self.paused = False
		self.played = True
		self.list.activate(self.current) 
		self.list.itemconfigure(self.current)

		mixer.music.play()

	#region PAUSE SONG	
	def pause_song(self):
		if not self.paused:
			self.paused = True
			mixer.music.pause()
			self.pause['image'] = pause
		else:
			if self.played == False:
				self.play_song()
			self.paused = False
			mixer.music.unpause()
			self.pause['image'] = play
	#endregion
	
	def prev_song(self):
		self.status_bar.config(text='')
		self.my_slider.config(to=0)
		if self.current > 0:
			self.current -= 1
		else:
			self.current = 0
		self.list.itemconfigure(self.current + 1, bg='white')
		self.play_song()

	def next_song(self):
		self.status_bar.config(text='')
		self.my_slider.config(to=0)
		if self.current < len(self.playlist) - 1:
			self.current += 1
		else:
			self.current = 0
		self.list.itemconfigure(self.current - 1, bg='white')
		self.play_song()
  
	def increase_volume(self, event=None):
		self.v = self.volume.get() + 1
		if self.v >= 10.0:
			self.v = 10.0
			mixer.music.set_volume((self.v)/10)
		self.volume.set(self.v)
		mixer.music.set_volume((self.v - 1)/10)
		print(self.v)
  
	def decrease_volume(self, event=None):
		self.v = self.volume.get() - 1
		if self.v <= 0.0:
			self.v = 0.0
			mixer.music.set_volume((self.v)/10)
		self.volume.set(self.v)
		mixer.music.set_volume((self.v + 1)/10)
		print(self.v)
  
	def change_volume(self, event=None):
		self.v = self.volume.get()
		mixer.music.set_volume(self.v / 10)
		print(self.v)

	def mute_volume(self, event=None):
		global muted
		self.v = self.volume.get()
		if muted:  # Unmute the music
			self.volume.set(self.v)
			mixer.music.set_volume(self.v / 10)
			muted = FALSE
		else:	# mute the music
			self.v = 0.0
			self.volume.set(self.v)
			mixer.music.set_volume(self.v / 10)
			muted = TRUE
		print(self.v)
  #endregion
 
	#region SONG DURATION 
	# grab song length time info
	def play_time(self):
		# time conversions
		current_time = mixer.music.get_pos()/1000
  
		#throw up temporary label
		converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))
  
		#Get song length with mutagen
		#have to have Queue open
		song = self.list.get(self.current)
		song = f"{self.folderpath}/{song}"		
		song_mut = MP3(song)
		global song_length
		song_length = song_mut.info.length
		converted_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))
		# increase current time
		current_time += 1
  
		if int(self.my_slider.get()) == int(current_time):
			# slider hasnt been moved
			# update slider to position
			slider_position = int(song_length)
			self.my_slider.config(to=slider_position)
			self.slider_value.set(int(current_time))
		elif self.paused == True:	
			pass
		else:
  			# slider has moved
			# update slider to position
			slider_position = int(song_length)
			self.my_slider.config(to=slider_position)
			self.slider_value.set(self.my_slider.get())
   
			converted_current_time = time.strftime('%H:%M:%S', time.gmtime(int(self.my_slider.get())))
   
			self.status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}        ')

			# move everything along by one second
			next_time = int (self.my_slider.get()) + 1
			self.slider_value.set(next_time)
  
		# update time
		self.status_bar.after(1000, self.play_time)
	#endregion

	#region Progress bar
	def slide(self,x):
		song = self.list.get(self.current)
		song = f"{self.folderpath}/{song}"			


		mixer.music.load(song)
		mixer.music.play(loops=0, start=int(self.slider_value.get()))

	#endregion
 
    #region Left Buttons
	def nav_widgets(self):
		#HOME
		self.homePage = ttk.Button(self.nav, style = 'TButton', command = self.openHomeWindow )
		self.homePage['text'] = 'Home'
		# self.homePage['command'] = self.go_home
		self.homePage.grid(row=0, column=0, padx=10, pady=10)

		#QUEUE
		self.queuePage = ttk.Button(self.nav, style = 'TButton', command = self.openQueueWindow)
		self.queuePage['text'] = 'Queue'
		self.queuePage.grid(row=2, column=0, padx=10, pady=5)
  
		#LIBRARY
		self.libPage = ttk.Button(self.nav, style = 'TButton', command = self.openLibraryWindow)
		self.libPage['text'] = 'Library'
		# self.libPage['command'] = self.go_lib
		self.libPage.grid(row=3, column=0, padx=10, pady=5)
  
		#HELP
		self.helpPage = ttk.Button(self.nav, style = 'TButton', command = self.openHelpWindow)
		self.helpPage['text'] = 'Help'
		# self.helpPage['command'] = self.go_help
		self.helpPage.grid(row=4, column=0, padx=10, pady=5)
 	 #endregion
  
    #region NEW WINDOWS
	# function to open a Queue Window
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
  
	# function to open a Library Window
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
  
	
	# function to open a Help Window
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
		self.muteInfo = tk.Label(self.HelpWindow, bg = 'blue', fg = 'white', font=("Gotham Medium typeface",font_size - 5,"bold"), text=text_) 
		# Anchor label to NW corner (top left)
		self.muteInfo.pack(anchor= 'nw')

		# Info about viewing the music library
		text_="""How to view your Library:\nYour music library comprises all of the songs that you have loaded into\nthe player from your device. You can view this by pressing the library\nbutton from the home screen. You can also sort your songs by different\ncriteria using the sort option(?). You can perform any normal actions\non these songs, such as adding to a playlist or the queue."""
		text_length = len(text_)
		font_size = int((w_h_ratio / text_length) / x)
		self.LibraryInfo = tk.Label(self.HelpWindow, bg = 'purple', fg = 'white', font=("Gotham Medium typeface",font_size + 3,"bold"), text=text_)
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
		text_= """Queue Information:\nYou can view your current queue by pressing the queue button on the\nhomepage. This will bring up a new window that will show what songs\nare next to be played and in what order they will be played."""
		text_length = len(text_)
		font_size = int((w_h_ratio / text_length) / x)
		self.queueInfo = tk.Label(self.HelpWindow, bg= 'green', fg = 'white', font=("Gotham Medium typeface",font_size - 5,"bold"), text= text_)
		# Anchor label to E corner (middle right)
		self.queueInfo.pack(anchor= 'e', pady= 10)

		# Label that tells how to make playlists
		text_ = """Creating a Playlist:\nNot sure if we are implementing this button, so this is just a placeholder for now.\n\n"""
		text_length = len(text_)
		font_size = int((w_h_ratio / text_length) / x)
		self.creatingPlaylists = tk.Label(self.HelpWindow, bg= '#E00DF9', fg = 'white', font=("Gotham Medium typeface",font_size - 30,"bold"), text=text_)
		# Anchor label to E corner (middle right)
		self.creatingPlaylists.pack(anchor= 'sw', pady= 1)
		# Button to open the additional help window

		self.moreHelp = tk.Button(self.HelpWindow, bg='#FF0000', fg= 'white', font=("Gotham Medium typeface", 13, "bold"))
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

	
	
  #endregion

#variables called into main
root = tk.Tk()
img = PhotoImage(file='images/Logo.png')
next_ = PhotoImage(file = 'images/next.gif')
prev = PhotoImage(file='images/previous.gif')
play = PhotoImage(file='images/play.gif')
pause = PhotoImage(file='images/pause.gif')
loadsongs = PhotoImage(file= 'images/loadsongs.png')
#add image variable here
  