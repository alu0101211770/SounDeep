# from operator import ge
# from pydub import AudioSegment
from clip import generateFeaturedClip
from split_wav import splitIntoFragments
from model import load_model
import os
import librosa
import numpy as np


def classify_theme(theme_file):
    if not os.path.exists('./tmp/'):
      os.makedirs('tmp')
    model = load_model('./model/model_architecture.json',
                      './model/model_weights.h5')
    clip = generateFeaturedClip(theme_file)
    splitIntoFragments(theme_file, clip, './tmp/')

    # mel_spectrograms will be an np.array with the shape [10, 128, 130, 1]
    # where 10 are the number of fragments, 128x130 the shape of the spectrogram
    # and a 1 is required as input of 2D convolution.
    mel_spectrograms = []
    for wav in os.listdir('./tmp/'):
        path = os.path.join('./tmp/', wav)
        y, sr = librosa.load(path, duration=3)
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000, hop_length=(
            (1 + np.array(y).shape[0]) // 129), n_fft=2048)
        mel_spectrograms.append(S)
        
    mel_spectrograms = np.array(mel_spectrograms)
    mel_spectrograms = mel_spectrograms.reshape(-1, 128, 130, 1)

    predictions = model.predict(mel_spectrograms)
    result = [[sum(prediction)/len(prediction)] for prediction in np.transpose(predictions)]
    genres = 'blues classical country disco pop hiphop metal reggae rock jazz'
    genres = genres.split()
    classified_genres = []
    for i in range(3):
      current_max_index = np.argmax(result)
      classified_genres.append(genres[current_max_index])
      del(result[current_max_index])
      del(genres[current_max_index])

    filelist = [ file for file in os.listdir('./tmp/') if file.endswith(".wav") ]
    for file in filelist:
      path_file = os.path.join('./tmp/', file)
      if os.path.exists(path_file):
        os.remove(path_file)

    return classified_genres