from cgitb import text
from email.mime import audio
from tkinter import *
from os import system
from turtle import color, left
import pygame
from tkinter import filedialog
import wave
from keras import layers
from keras.layers import (Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, 
                          Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D, Dropout, LSTM)
from keras.models import Model, Sequential, model_from_json
from keras.preprocessing import image
from keras.utils import layer_utils
from clip import *
import librosa
import librosa.display
import numpy as np
import matplotlib 
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import ImageTk,Image,ImageOps

root = Tk()
root.title('SounDeep')
root.geometry("600x400")
logo = PhotoImage(file="./GUI/img/logonormal.png")
root.iconphoto(False, logo)
menu = Menu(root, tearoff=False)
root.config(menu=menu)
subMenu = Menu(root, tearoff=False)
menu.add_cascade(label="File", menu=subMenu)
pygame.init()
audioFile = None
resultText = "Not yet predicted"

def playOriginal():
  global audioFile
  print(audioFile)
  if (audioFile != None):
    pygame.mixer.music.load(audioFile)
    pygame.mixer.music.play(loops=0)
  else: 
    createAlert()

def spectogram():
  y,sr = librosa.load('./audio/best-moment.wav', duration=3)
  S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000, hop_length=((1 + np.array(y).shape[0]) // 64), n_fft=2048)
  #S = librosa.feature.melspectrogram(y=y, sr=sr)
  fig = plt.figure()
  canvas = FigureCanvas(fig)
  #plt.imsave('specto.png', librosa.power_to_db(S,ref=np.max))
  #plt.imshow(librosa.power_to_db(S,ref=np.max))
  #librosa.display.specshow(librosa.power_to_db(S,ref=np.max))
  model = load_model()
  print(model)
  #predicted = model.predict()
  #global resulText
  #resultText = predicted
  plt.show()
  root.mainloop()
  ''''
  myImage = ImageTk.PhotoImage(image)
  window = Toplevel(root)
  window.title('specto')
  imgLabel = Label(window, image=myImage, text='specto')
  imgLabel.pack()
  window.mainloop()
  '''

def stopOriginal():
  pygame.mixer.music.stop()

def stopCutVersion():
  pygame.mixer.music.stop()

def loadAudio():
  global audioFile
  filename = filedialog.askopenfilename(initialdir="/Images", title="Select a File", filetypes=[('Wav files', '*.wav'), ('Mp3 files', '*.mp3')])
  #audio = wave.open(filename)
  audioFile = filename
  generateFeaturedClip(audioFile, 30)
  spectogram()

def playCutVersion():
  if (audioFile != None):
    pygame.mixer.music.load('./audio/best-moment.wav')
    pygame.mixer.music.play(loops=0)
  else: 
    createAlert()

def createAlert():
  alert = Toplevel(root)
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
  
def quitr():
  root.destroy()

def load_model():
  model = model_from_json(open('./model/model_architecture.json').read())
  model.load_weights('./model/model_weights.h5')
  #model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy', get_f1])
  return model
 
def on_enter(e):
  e.widget['background'] = '#7393BC'
def on_leave(e):
  e.widget['background'] = 'SystemButtonFace'


# Labels, buttons, UI stuff
main_frame = Frame(root, width=600, height=400)
main_frame.pack()
img = Image.open("./GUI/img/logopequeño.png")
bgImg = Image.open("./GUI/img/background2.png")
welcomeImg = Image.open("./GUI/img/welcomef.png")
bgImg.paste(img,(480,300), img)
bgImg.paste(welcomeImg,(140,20),welcomeImg)
bgImg.save('./GUI/img/NewImg.png',"PNG")
bg = PhotoImage(file="./GUI/img/NewImg.png")
bgLabel = Label(main_frame, image=bg)
bgLabel.place(x = 0, y = 0)
#welcomeLabel = Label(main_frame,image=welcomeImg,font=("Modern",22))
#welcomeLabel.place(x=140,y=20)
originalLabel = Label(main_frame, text="Original song: ",font=("Modern",12))
originalLabel.place(x=50,y=120)
play_button = Button(root, text="Play song  ", font=("Modern", 16), command=playOriginal)
play_button.place(x=180,y=110)
play_button.bind("<Enter>", on_enter)
play_button.bind("<Leave>", on_leave)
stop_button = Button(root, text="Stop song", font=("Modern", 16), command=stopOriginal)
stop_button.place(x=320,y=110)
stop_button.bind("<Enter>", on_enter)
stop_button.bind("<Leave>", on_leave)
clipLabel = Label(main_frame, text="Clipped song: ",font=("Modern",12))
clipLabel.place(x=50,y=260)
clip_button = Button(root, text="Play clip  ",background="#3C85C7", font=("Modern", 16), command=playCutVersion)
clip_button.place(x=180,y=240)
clip_button.bind("<Enter>", on_enter)
clip_button.bind("<Leave>", on_leave)
clip_stop_button = Button(root, text="Stop clip", font=("Modern", 16), command=stopCutVersion)
clip_stop_button.place(x=320,y=240)
clip_stop_button.bind("<Enter>", on_enter)
clip_stop_button.bind("<Leave>", on_leave)
predictLabel = Label(main_frame, text="Prediction: ",font=("Modern",12))
resultLabel = Label(main_frame, text=resultText,font=("Modern",12))
resultLabel.configure(background="#DFA01F")
resultLabel.place(x=180,y=340)
predictLabel.place(x=50,y=340)
subMenu.add_command(label="Load", command=loadAudio)
root.protocol("WM_DELETE_WINDOW", quitr)
root.mainloop()