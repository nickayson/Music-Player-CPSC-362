from msilib.schema import TextStyle
import os
import pickle
import tkinter as tk
import time

from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer

from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen import MutagenError

'''
THINGS TO DO:
Home page
	- fix gap above buttons

Volume slider buttons and formatting
	- just need button commands/functions

Change play buttons and everything

Make song scaler at bottom

Make Login Page
 
Make Library Page

Make Queue Page
'''

'''
NOTES:

we could use ttk.Progressbar for the song scaler --> https://docs.python.org/3/library/tkinter.ttk.html 
theres a weird gap above all the labels? not sure why or how to fix it
-ashley

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
		# directory = filedialog.askdirectory()
		# for root_, dirs, files in os.walk(directory):
		# 		for file in files:
		# 			if os.path.splitext(file)[1] == '.mp3':
		# 				path = (root_ + '/' + file).replace('\\','/')
		song = f"C:/Users/Nick's Laptop/Music/Music/{song}"
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
		song = f"C:/Users/Nick's Laptop/Music/Music/{song}"

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
	
	# function to open a Help Window
	def openHelpWindow(self):
     # Instructions for each button and how to navigate around the app
		self.HelpWindow = Toplevel(root)
		self.HelpWindow.title("Help")
		width= root.winfo_screenwidth() 
		height= root.winfo_screenheight()
		self.HelpWindow.geometry("%dx%d" % (width, height))

		self.HelpWindow['bg'] = 'black'

		######### Overall title for the help page
		self.helpTitle = tk.Label(self.HelpWindow, bg = 'black', fg = 'white', font=("Gotham Medium typeface",20,"bold")
                            , text="Welcome to the Help Page" )	
		#Put in text description of what the software does and why we created it with the logo.png photo
		# self.helpTitle.config(width=23,height=1)
		self.helpTitle.grid(row=0, column=0, padx=10)
		# self.helpTitle.insert(tk.END, Description)

		######### Title for description of the mute button function
		self.muteTitle = tk.Label(self.HelpWindow, bg = 'blue', fg = 'white', font=("Gotham Medium typeface",10,"bold"),
                          text="Mute button information:"  )
		# self.muteTitle.config(width=22, height=1)
		self.muteTitle.grid(row=10, column=0, padx= 10, pady=10)
		# self.muteTitle.insert(tk.END,Description)

		######### Description for mute button function
		self.muteText = tk.Label(self.HelpWindow, bg = 'blue', fg = 'white', font=("Gotham Medium typeface",12,"bold"),
					text = "Our mute button will record your volume level from\nbefore mute was hit; this level will be restored\nupon being unmuted. The volume can be unmuted\nby interacting with any of the volume control\nbuttons or the slider.")
		# self.muteText.config(width= 43, height=5)
		self.muteText.grid(row=15, column=0, padx= 0, pady=10)
		# self.muteText.insert(tk.END, Description)

		######### Title for 'Load Song' Description
		self.loadsongTitle = tk.Label(self.HelpWindow, bg = 'purple', fg = 'white', font=("Gotham Medium typeface",20,"bold"),
		            text= "Loading Songs:")	
		#Put in text description of what the software does and why we created it with the logo.png photo
		# self.loadsongTitle.config(width=14,height=1)
		self.loadsongTitle.grid(row=10, column=35, padx=0, pady=10)
  

		######## Description of how to load songs
		self.loadsongsInfo = tk.Label(self.HelpWindow, bg = 'purple', fg = 'white', font=("Gotham Medium typeface",12,"bold"))	
		#Put in text description of what the software does and why we created it with the logo.png photo
		Description = """You can easily add songs from your computer by\nuploading them as files. Simply click on the "Load\nSong" button to bring up a window from which you can navigate through your files to find songs to\nupload. One a song has been uloaded, it will appear in your library.(?)"""
		self.loadsongsInfo.grid(row=15, column=35, padx=0, pady=10)
  

		self.loadsongsbutton = tk.Label(self.HelpWindow, image=loadsongs)
		self.loadsongsbutton.configure(width=225, height=100)
		self.loadsongsbutton.grid(row=1,column=0, padx= 0, pady=0)
	
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
  