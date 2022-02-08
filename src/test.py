import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import clip

audio_file = ''
short_audio = ''

def loadAudio():
    global audio_file, short_audio
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=[('Wav files', '*.wav')])
    audio_file = filename  if filename != '' else audio_file
    if (audio_file != ''):
        short_audio = clip.generateFeaturedClip(audio_file, 30) 

root = tk.Tk()

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
add_theme_button = ttk.Button(theme, text="Add theme", command = loadAudio)
test_button = ttk.Button(theme, text="test")

content.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
title.grid(columnspan=2)
theme.grid(column=0, row=1, columnspan=2)
add_theme_button.grid(column=0, row=0)
test_button.grid(column=0, row=1)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

content.columnconfigure(0, weight=1)
content.columnconfigure(1, weight=1)
content.rowconfigure(0, weight=1)
content.rowconfigure(1, weight=1)

theme.rowconfigure(0, weight=1)
theme.columnconfigure(0, weight=1)


root.mainloop()

