from pydub import AudioSegment

def getFileName(filePath):
  return filePath.split("/")[-1].split(".")[0]

def splitIntoFragments(file, audio, outputDirectory):
  fileName = getFileName(file)
  fragmentDuration = 3000
  print(audio.duration_seconds)
  numberOfFragments = int(audio.duration_seconds / 3)
  for i in range(numberOfFragments):
    newAudio = audio[i * fragmentDuration : i * fragmentDuration + fragmentDuration]
    newAudio.export(outputDirectory + fileName + '_' + str(i) + '.wav', format="wav")