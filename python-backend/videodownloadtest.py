import pafy
import os
from deepgram_test import *
from text_parser import *

url = "https://www.youtube.com/watch?v=3UAOs9B9UH8"

video = pafy.new(url)

audio = video.audiostreams
choice = audio[0]
for a in audio:
    if(a.extension == "webm"):
        choice = a
choice.download()
transcript = process(choice.filename)
os.remove(choice.filename)
process_sentence_block(choice.filename, *transcript)


