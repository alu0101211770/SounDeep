from pydub import AudioSegment
from clip import generateFeaturedClip
from split_wav import splitIntoFragments
from model import load_model
import os
import librosa
import numpy as np

model = load_model('./model/model_architecture.json',
                   './model/model_weights.h5')

# def process_wav():
#   return 0

audio_file = './audio/blues.00000.wav'
audio = AudioSegment.from_wav(audio_file)
clip = generateFeaturedClip(audio)
splitIntoFragments(audio_file, clip, './tmp/')

# Crear un array y meter cada espectrograma de mel en el array (que tenga la shape correcta)

for wav in os.listdir('./tmp/'):
    print(wav)
    path = os.path.join('./tmp/', wav)
    y, sr = librosa.load(path, duration=3)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000, hop_length=(
        (1 + np.array(y).shape[0]) // 129), n_fft=2048)
