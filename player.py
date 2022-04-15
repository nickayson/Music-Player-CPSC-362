import os
import pickle
import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer

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
		#self.tracklist_widgets()
		self.nav_widgets()
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

	#region VOLUME_WIDGET
	def volume_widgets(self):
	    #VOLUME SLIDER
		self.volume = tk.DoubleVar(self)
		self.slider = tk.Scale(self.volumew, from_ = 10, to = 0, bg = 'black', fg = 'white' ) #from_ x = top value, to x = bottom value
		self.slider['variable'] = self.volume
		self.volume.set(8)
		mixer.music.set_volume(0.8)
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

		self.pause['image'] = play
		self.paused = False
		self.played = True
		self.list.activate(self.current) 
		self.list.itemconfigure(self.current, bg='sky blue')

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
		if self.current > 0:
			self.current -= 1
		else:
			self.current = 0
		self.list.itemconfigure(self.current + 1, bg='white')
		self.play_song()

	def next_song(self):
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
  
#   muted = FALSE


# def mute_music():
#     global muted
#     if muted:  # Unmute the music
#         mixer.music.set_volume(0.7)
#         volumeBtn.configure(image=volumePhoto)
#         scale.set(70)
#         muted = FALSE
#     else:  # mute the music
#         mixer.music.set_volume(0)
#         volumeBtn.configure(image=mutePhoto)
#         scale.set(0)
#         muted = TRUE
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

  #region HOME BUTTON
	def nav_widgets(self):
		#HOME
		self.homePage = ttk.Button(self.nav, style = 'TButton')
		self.homePage['text'] = 'Home'
		# self.homePage['command'] = self.go_home
		self.homePage.grid(row=0, column=0, padx=10, pady=10)

		#HELP
		self.helpPage = ttk.Button(self.nav, style = 'TButton', command = self.openHelpWindow)
		self.helpPage['text'] = 'Help'
		# self.helpPage['command'] = self.go_help
		self.helpPage.grid(row=1, column=0, padx=10, pady=5)

		#LIBRARY
		self.libPage = ttk.Button(self.nav, style = 'TButton', command = self.openLibraryWindow)
		self.libPage['text'] = 'Library'
		# self.libPage['command'] = self.go_lib
		self.libPage.grid(row=2, column=0, padx=10, pady=5)


		#QUEUE
		self.queuePage = ttk.Button(self.nav, style = 'TButton', command = self.openQueueWindow)
		self.queuePage['text'] = 'Queue'
		self.queuePage.grid(row=3, column=0, padx=10, pady=5)

		#PROFILE
		self.profPage = ttk.Button(self.nav, style = 'TButton')
		self.profPage['text'] = 'Profile'
		# self.queuePage['command'] = self.go_queue
		self.profPage.grid(row=4, column=0, padx=10, pady=5)	
  #endregion
  
  #region NEW WINDOWS
	# function to open a Queue Window
	def openQueueWindow(self):
		self.QueueWindow = Toplevel(root)
		self.QueueWindow.title("Queue")
		width= root.winfo_screenwidth() 
		height= root.winfo_screenheight()
		self.QueueWindow.geometry("%dx%d" % (width, height))

		self.QueueWindow['bg'] = 'black'
  
		label5 = tk.Label(self.QueueWindow, bg = 'black', fg = 'white', font=("Gotham Medium typeface",16,"bold"), text='Queue')
		self.tracklist = ttk.LabelFrame(self.QueueWindow, labelwidget=label5)
		# self.tracklist.config(width=1200,height=600)
		self.tracklist.grid(row=0, column=1, rowspan=3, pady=5)
		
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
		LibraryWindow = Toplevel(root)
		LibraryWindow.title("Library")
		width= root.winfo_screenwidth() 
		height= root.winfo_screenheight()
		LibraryWindow.geometry("%dx%d" % (width, height))
	
	# function to open a Help Window
	def openHelpWindow(self):
		HelpWindow = Toplevel(root)
		HelpWindow.title("Library")
		width= root.winfo_screenwidth() 
		height= root.winfo_screenheight()
		HelpWindow.geometry("%dx%d" % (width, height))
  #endregion

#variables called into main
root = tk.Tk()
img = PhotoImage(file='images/Logo.png')
next_ = PhotoImage(file = 'images/next.gif')
prev = PhotoImage(file='images/previous.gif')
play = PhotoImage(file='images/play.gif')
pause = PhotoImage(file='images/pause.gif')
  