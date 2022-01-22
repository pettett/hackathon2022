import pafy
import os

url = "https://www.youtube.com/watch?v=rqWClsdVFOU"

video = pafy.new(url)

audio = video.audiostreams
choice = audio[0]
for a in audio:
    if(a.get_filesize() < choice.get_filesize()):
        choice = a
print(choice.filename)
choice.download()
#os.remove("AudioFile")

