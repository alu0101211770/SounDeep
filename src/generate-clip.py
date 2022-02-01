from pydub import AudioSegment

def mean(array):
  sum = 0
  for element in array:
    sum += abs(element)
  return sum / len(array)

def generateFeaturedClip(file, second_rate):
  audio = AudioSegment.from_wav(file)
  best_mean = 0
  best_second = 0
  for i in range(round((int(audio.duration_seconds) - 30) / second_rate)):
    newAudio = audio[i*second_rate*1000:30000+i*second_rate*1000]
    newMean = mean(newAudio.get_array_of_samples())
    if (newMean > best_mean):
      print(i * second_rate)
      best_mean = newMean
      best_second = i * 1000 * second_rate
      print(best_mean)
  newAudio = audio[best_second:30000+best_second]
  newAudio.export('best-moment.wav', format="wav")

# generateFeaturedClip("phaseone.wav", 1)
