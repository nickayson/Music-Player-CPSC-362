import os
import pickle
import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer

def change_volume(self, event=None):
    self.v = self.volume.get()
    mixer.music.set_volume(self.v / 10)