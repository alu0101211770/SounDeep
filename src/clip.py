from pydub import AudioSegment
from split_wav import getFileName
import os

def mean(array):
  """
  Calculates the mean of the absolute values in a list of numbers
  
  Args:
    array (list): array which we want to calculate the mean
  
  Returns:
    float: mean of the absolute values of the elements of the array
  """
  sum = 0
  for element in array:
    sum += abs(element)
  return sum / len(array)

def generateFeaturedClip(audio_file):
  """
  Generates a 30 seconds clip with the loudest part of the audio
  
  Args:
    file (string): path of the wav file
    second_rate (integer): every how many seconds a 30 second check will be done
  """
  audio = AudioSegment.from_wav(audio_file)
  second_rate = int(audio.duration_seconds * 0.1)
  best_mean = 0
  best_second = 0
  for i in range(round((int(audio.duration_seconds) - 30) / second_rate)):
    newAudio = audio[i*second_rate*1000:30000+i*second_rate*1000]
    newMean = mean(newAudio.get_array_of_samples())
    if (newMean > best_mean):
      best_mean = newMean
      best_second = i * 1000 * second_rate
  newAudio = audio[best_second:30000+best_second]
  if os.path.exists('./audio/best-moment.wav'):
    os.remove('./audio/best-moment.wav')
  newAudio.export('./audio/' + 'best-moment' + '.wav', format="wav")

  return newAudio
