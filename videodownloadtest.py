import pafy
import os
from deepgram_test import *

url = "https://www.youtube.com/watch?v=r5OPTj7fKVw"

video = pafy.new(url)

audio = video.audiostreams
choice = audio[0]
for a in audio:
    if(a.get_filesize() < choice.get_filesize()):
        choice = a
choice.download()
test = process(choice.filename)
os.remove(choice.filename)

