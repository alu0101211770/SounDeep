import tkinter as tk
from tkinter import Button, Label, filedialog
from tkinter import ttk
from classify import classify_theme
import clip
import pygame
from PIL import ImageTk, Image
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os

audio_file = ''
short_audio = ''
is_paused = False
is_paused_fr = False
already = False
already_fr = False
load1 = False
load2 = False
result = 'Not yet'
root = tk.Tk()
pygame.init()
content = tk.Frame(root)
spectrogram = ttk.Frame(content)
mel = ttk.Label(spectrogram, image='')


def loadAudio():
    global audio_file, short_audio, theme, load1
    filename = filedialog.askopenfilename(
        initialdir="./", title="Select a File", filetypes=[('Wav files', '*.wav')])
    audio_file = filename if filename != '' else audio_file
    if (audio_file != ''):
        short_audio = clip.generateFeaturedClip(audio_file)
        pygame.mixer.music.load(audio_file)
        load1 = True
        generateMel(mel)
        print(audio_file)


def createAlert():
    alert = tk.Toplevel(root)
    window_height = 100
    window_width = 250
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    alert.geometry("{}x{}+{}+{}".format(window_width,
                                        window_height, x_cordinate, y_cordinate - 200))
    alertLabel = Label(alert, text="Please load a song")
    alertLabel.pack()
    alert.after(5000, lambda: alert.destroy())
    alert.mainloop()


def playThemeAudio():
    global audio_file, is_paused, already, already_fr, load1, load2
    if (not load1):
        pygame.mixer.music.load(audio_file)
        load1 = True
        load2 = False
        is_paused = True
    if (audio_file != ''):
        if (is_paused and already):
            pygame.mixer.music.unpause()
            is_paused = False
        elif (not is_paused and already):
            pygame.mixer.music.pause()
            is_paused = True
        else:
            pygame.mixer.music.play(loops=0)
            already = True
            is_paused = False
    else:
        createAlert()


def stopThemeAudio():
    global load1, already
    pygame.mixer.music.stop()
    load1 = False
    already = False


def playFragmentAudio():
    global short_audio, is_paused_fr, already_fr, load1, load2
    if (not load2):
        pygame.mixer.music.load('./audio/best-moment.wav')
        load2 = True
        load1 = False
        is_paused_fr = True
    if (short_audio != ''):
        if (is_paused_fr and already_fr):
            pygame.mixer.music.unpause()
            is_paused_fr = False
        elif (not is_paused_fr and already_fr):
            pygame.mixer.music.pause()
            is_paused_fr = True
        else:
            pygame.mixer.music.play(loops=0)
            already_fr = True
            is_paused_fr = False
    else:
        createAlert()


def stopFragmentAudio():
    global load2, already_fr
    pygame.mixer.music.stop()
    load2 = False
    already_fr = False


def predict(label):
    global result, root, load1, load2, already, already_fr
    pygame.mixer.music.unload()
    load1 = False
    load2 = False
    already = False
    already_fr = False
    results = classify_theme('./audio/best-moment.wav')
    results_string = f'Predicted:\n1.{results[0]}\n2.{results[1]}\n3.{results[2]}'
    label.configure(text=results_string)


def generateMel(label):
    y, sr = librosa.load('./audio/best-moment.wav', duration=30)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000, hop_length=(
        (1 + np.array(y).shape[0]) // 129), n_fft=2048)
    # fig = plt.figure()
    fig, ax = plt.subplots()
    S_dB = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_dB, x_axis='time',
                                   y_axis='mel', sr=sr,
                                   fmax=8000, ax=ax)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set(title='Mel-frequency spectrogram')
    plt.savefig('./GUI/img/spectrogram.png')
    img = Image.open('./GUI/img/spectrogram.png')
    final = img.resize((int(img.size[0]/2), int(img.size[1]/2)))
    spectro = ImageTk.PhotoImage(final)
    label.configure(image=spectro)
    root.mainloop()


def quitr():
    root.destroy()


root.minsize(250, 250)
root.title("SounDeep")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
logo = tk.PhotoImage(file="./GUI/img/logonormal.png")
root.iconphoto(False, logo)


title = tk.Label(content, text="Welcome to SounDeep!",
                 font=('Times 14'), height=3)

theme = ttk.Frame(content)
audio_fragment = ttk.Frame(content)
classify = ttk.Frame(content)

add_theme_button = ttk.Button(theme, text="Load theme", command=loadAudio)
playOriginal = ttk.Button(
    theme, text="Play/Pause theme", command=playThemeAudio)
stopOriginal = ttk.Button(theme, text="Stop theme", command=stopThemeAudio)
playFragment = ttk.Button(
    audio_fragment, text="Play/Pause clip", command=playFragmentAudio)
stopFragment = ttk.Button(
    audio_fragment, text="Stop clip", command=stopFragmentAudio)
test_result = ttk.Label(classify, text=result, font=('Times, 14'))
test_button = ttk.Button(classify, text="Classify",
                         command=lambda: predict(test_result))

content.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
title.grid(column=0, row=0, columnspan=4)
theme.grid(column=2, row=1)
classify.grid(column=2, row=3)
audio_fragment.grid(column=1, row=2)
spectrogram.grid(column=2, row=2)
playOriginal.grid(column=2, row=2, pady=10)
stopOriginal.grid(column=2, row=3)
add_theme_button.grid(column=2, row=1)
playFragment.grid(column=1, row=2, pady=10, padx=10)
stopFragment.grid(column=1, row=3, padx=10)
test_button.grid(column=0, row=0, columnspan=2, pady=10)
test_result.grid(column=0, row=1, columnspan=2, pady=10)
mel.grid(column=2, row=2)

root.columnconfigure(0, weight=2)
root.rowconfigure(0, weight=2)

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
content.rowconfigure(3, weight=1)

theme.rowconfigure(0, weight=1)
theme.columnconfigure(0, weight=1)
theme.rowconfigure(0, weight=1)

audio_fragment.rowconfigure(0, weight=1)
audio_fragment.columnconfigure(0, weight=1)
audio_fragment.rowconfigure(1, weight=1)
audio_fragment.columnconfigure(1, weight=1)
audio_fragment.rowconfigure(2, weight=1)
audio_fragment.columnconfigure(2, weight=1)
audio_fragment.rowconfigure(3, weight=1)
audio_fragment.columnconfigure(4, weight=1)

root.protocol("WM_DELETE_WINDOW", quitr)
root.mainloop()
