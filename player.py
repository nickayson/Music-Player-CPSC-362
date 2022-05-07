from msilib.schema import TextStyle
import os
import pickle
import tkinter as tk
import time

from tkinter import *
from tkinter import ttk
from tkinter import font
from turtle import bgcolor, color, home
from ttkthemes import ThemedTk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer

from home import Home
from help import Help
from library import Library
from qlist import QPage
from main import *

from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen import MutagenError

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
		
		self.read_folderpath()
		# self.reload_songs()
		self.create_frames()
		self.track_widgets()
		self.control_widgets()
		self.volume_widgets()
		self.nav_widgets()
		self.progress_widgets()
  #endregion
  
    #region CREATE_FRAMES
	def create_frames(self):
    	# REMOVE SONGS
		self.remove_songs()

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
		self.loadSongs = ttk.Button(self.controls, style = 'TButton', command=lambda:[self.QueueWindow(), self.retrieve_songs()])
		self.loadSongs['text'] = 'Load Songs'
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
	#endregion

    #region RETRIEVE SONGS
	def retrieve_songs(self):
        #FILE SEARCHER
		self.songlist = []
		directory = filedialog.askdirectory()
		for root_, dirs, files in os.walk(directory):
				for file in files:
					if os.path.splitext(file)[1] == '.mp3':
						self.set_folderpath(root_)
						global path
						path = (root_ + '/' + file).replace('\\','/')
						self.songlist.append(path)


		with open('songs.pickle', 'wb') as f:
			pickle.dump(self.songlist, f)
		self.playlist = self.songlist
		self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
		self.list.delete(0, tk.END)
		self.enumerate_songs()
		self.play_song()
	#endregion

	#region GET FOLDER PATH
	def read_folderpath(self):
		with open('folder_path.txt', 'r') as f:
			data = f.read()
			if data:
				self.folderpath = data
	#endregion

	#region SAVE FOLDER PATH
	def set_folderpath(self, path):
		self.folderpath = path
		with open('folder_path.txt', 'w') as f:
			f.write(path)
	#endregion
 
	#region Library search
	def searchfiles(self):
		self.liblist = []
		directory = filedialog.askdirectory()
		count = 0
		
		for root_, dirs, files in os.walk(directory):
			for file in files:
				if os.path.splitext(file)[1] == '.mp3':
						self.set_folderpath(root_)
						global path
						path = (root_ + '/' + file).replace('\\','/')
						# self.liblist.append(self.folderpath2)
						self.liblist.append(path)
						count += 1
				if count == 0:
					self.folderpath2 = root_
					self.liblist.append(self.folderpath2)
					self.liblist.append("============================================================================================")
		with open('songs.pickle', 'wb') as f:
			pickle.dump(self.liblist, f)
		self.playlist = self.liblist
		self.list.delete(0, tk.END)
		self.enumerate_songs()
	#endregion

	#region RELOAD SONGS
	def reload_songs(self):
		if(self.folderpath != ""):
			self.liblist = []
			directory = self.folderpath
			count = 0
			
			for root_, dirs, files in os.walk(directory):
				for file in files:
					if os.path.splitext(file)[1] == '.mp3':
							self.set_folderpath(root_)
							global path
							path = (root_ + '/' + file).replace('\\','/')
							# self.liblist.append(self.folderpath2)
							self.liblist.append(path)
							count += 1
					if count == 0:
						self.folderpath2 = root_
						self.liblist.append(self.folderpath2)
						self.liblist.append("============================================================================================")
			with open('songs.pickle', 'wb') as f:
				pickle.dump(self.liblist, f)
			self.playlist = self.liblist
			self.list.delete(0, tk.END)
			self.enumerate_songs()
	#endregion
 
	#region REMOVE SONGS
	def remove_songs(self):
		self.empty = []
		with open('filename', 'wb') as f:
			pickle.dump(self.empty, f)
		self.playlist = self.empty
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
				self.list.itemconfigure(i)
				
    
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
		# print(self.v)
  
	def decrease_volume(self, event=None):
		self.v = self.volume.get() - 1
		if self.v <= 0.0:
			self.v = 0.0
			mixer.music.set_volume((self.v)/10)
		self.volume.set(self.v)
		mixer.music.set_volume((self.v)/10)
		# print(self.v)
  
	def change_volume(self, event=None):
		self.v = self.volume.get()
		mixer.music.set_volume(self.v / 10)
		# print(self.v)

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
  
		if converted_current_time == converted_song_length:
			self.next_song()
	#endregion

	#region Progress bar
	def slide(self,x):
		song = self.list.get(self.current)
		song = f"{self.folderpath}/{song}"			


		mixer.music.load(song)
		mixer.music.play(loops=0, start=int(self.slider_value.get()))
		if(self.paused == True):
			mixer.music.pause()

	#endregion
 
    #region Left Buttons
	def nav_widgets(self):
		#HOME
		self.homePage = ttk.Button(self.nav, style = 'TButton', command = self.HomeWindow)
		self.homePage['text'] = 'Home'
		# self.homePage['command'] = self.go_home
		self.homePage.grid(row=0, column=0, padx=10, pady=10)

		#QUEUE
		self.queuePage = ttk.Button(self.nav, style = 'TButton', command = self.QueueWindow)
		self.queuePage['text'] = 'Queue'
		self.queuePage.grid(row=2, column=0, padx=10, pady=5)
  
		#LIBRARY
		self.libPage = ttk.Button(self.nav, style = 'TButton', command = self.LibraryWindow)
		self.libPage['text'] = 'Library'
		# self.libPage['command'] = self.go_lib
		self.libPage.grid(row=3, column=0, padx=10, pady=5)
  
		#HELP
		self.helpPage = ttk.Button(self.nav, style = 'TButton', command = self.HelpWindow)
		self.helpPage['text'] = 'Help'
		# self.helpPage['command'] = self.go_help
		self.helpPage.grid(row=4, column=0, padx=10, pady=5)
 	 #endregion
  
    # region NEW WINDOWS
	def HomeWindow(self):
		Home.openHomeWindow(self)
  
	def QueueWindow(self):
		self.remove_songs()
		QPage.openQueueWindow(self)
  
	# function to open a Library Window
	def LibraryWindow(self):
		self.remove_songs()
		Library.openLibraryWindow(self)
  
	# function to open a Help Window
	def HelpWindow(self):
		Help.openHelpWindow(self)
  #endregion

#app to be deployed
app = Player(master=root)
app['bg'] = 'black'
app.mainloop()

  