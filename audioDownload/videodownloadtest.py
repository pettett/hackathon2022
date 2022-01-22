import pafy
import os

url = "https://www.youtube.com/watch?v=PbBzhqJK3bg&t=1582s"

video = pafy.new(url)

audio = video.audiostreams
choice = audio[0]
for a in audio:
    if(a.get_filesize() < choice.get_filesize()):
        choice = a
choice.download()
os.remove(choice.filename)

