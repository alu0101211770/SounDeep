import tkinter as tk
from tkinter import Button, Label, filedialog
from tkinter import ttk
import clip
import pygame
from PIL import ImageTk, Image

audio_file = ''
short_audio = ''
is_paused = False
already = False
result = 'Not yet'
theme = None
root = tk.Tk()
pygame.init()

def loadAudio():
    global audio_file, short_audio, theme
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=[('Wav files', '*.wav')])
    audio_file = filename  if filename != '' else audio_file
    if (audio_file != ''):
      #short_audio = clip.generateFeaturedClip(audio_file)
      theme = pygame.mixer.Sound(audio_file) 

def playThemeAudio():
  global audio_file, is_paused, already, theme
  print(theme)
  if (audio_file != ''):
    if (is_paused and already):
      theme.unpause()
      is_paused = False
    elif (not is_paused and already):
      theme.pause()
      is_paused = True
    else:
      theme.play(loops=0)
      already = True
  else: 
    createAlert()


def stopThemeAudio():
  theme.stop()

def playFragmentAudio():
  pass

def stopFragmentAudio():
  pass

def predict():
  #results = clasify()
  pass
def showMel():
  y,sr = librosa.load('.audio/best-moment.wav', duration=30)
  S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000, hop_length=((1 + np.array(y).shape[0]) // 64), n_fft=2048)
  fig = plt.figure()
  plt.imsave('./GUI/img/spectrogram.png', librosa.power_to_db(S,ref=np.max))

def createAlert():
  alert = tk.Toplevel(root)
  window_height = 100
  window_width = 250
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  x_cordinate = int((screen_width/2) - (window_width/2))
  y_cordinate = int((screen_height/2) - (window_height/2))
  alert.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate - 200))
  alertLabel = Label(alert,text="Please load a song")
  alertLabel.pack()
  alert.after(5000, lambda: alert.destroy())
  alert.mainloop()

root.minsize(250, 250)
root.title("SounDeep")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
logo = tk.PhotoImage(file="./GUI/img/logonormal.png")
root.iconphoto(False, logo)

content = tk.Frame(root)
title = tk.Label(content, text="Welcome to SounDeep!", font=('Times 14'), height = 3)

theme = ttk.Frame(content)
audio_fragment = ttk.Frame(content)
spectrogram = ttk.Frame(content)
clasify = ttk.Frame(content)

add_theme_button = ttk.Button(theme, text="Add theme", command = loadAudio)
playOriginal = ttk.Button(theme, text="Play/Pause theme", command=playThemeAudio)
stopOriginal = ttk.Button(theme, text="Stop theme", command=stopThemeAudio)
playFragment = ttk.Button(audio_fragment, text="Play/Pause clip", command=playFragmentAudio)
stopFragment = ttk.Button(audio_fragment, text="Stop clip", command=stopFragmentAudio)
test_button = ttk.Button(clasify, text="test", command=predict)
test_result = ttk.Label(clasify, text=result, font=('Times, 14'))
specto = ImageTk.PhotoImage(Image.open('./GUI/img/spectrogram.png'))
mel = ttk.Label(audio_fragment, image=specto)
content.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
title.grid(column= 0, row= 0, columnspan=2)
theme.grid(column=1, row=1)
clasify.grid(column=0, row=3, columnspan=2)
audio_fragment.grid(column=0, row=2, columnspan=4)
playOriginal.grid(column=2,row=2)
stopOriginal.grid(column=2,row=3)
add_theme_button.grid(column=2, row=1)
playFragment.grid(column=2,row=2)
stopFragment.grid(column=2,row=3)
test_button.grid(column=3, row=2)
test_result.grid(column=3,row=3, columnspan=3)
mel.grid(column=4,row=2)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

content.columnconfigure(0, weight=1)
content.columnconfigure(1, weight=1)
content.columnconfigure(2, weight=1)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(0, weight=1)
content.rowconfigure(1, weight=1)
content.rowconfigure(1, weight=1)
content.rowconfigure(2, weight=1)
content.rowconfigure(2, weight=1)
content.rowconfigure(3,weight=1)

theme.rowconfigure(0, weight=1)
theme.columnconfigure(0, weight=1)
theme.rowconfigure(0,weight=1)

audio_fragment.rowconfigure(0, weight=1)
audio_fragment.columnconfigure(0, weight=1)
audio_fragment.rowconfigure(1, weight=1)
audio_fragment.columnconfigure(1, weight=1)
audio_fragment.rowconfigure(2, weight=1)
audio_fragment.columnconfigure(2, weight=1)
audio_fragment.rowconfigure(3, weight=1)
audio_fragment.columnconfigure(4, weight=1)

root.mainloop()

