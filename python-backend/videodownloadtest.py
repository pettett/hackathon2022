import pafy
import os
from deepgram_test import *
from text_parser import *

#url = "https://www.youtube.com/watch?v=jq_Kh2rV3x8"
#url = "https://www.youtube.com/watch?v=xxHFkOff9T8"
url = "https://www.youtube.com/watch?v=VdHmgkkVYec"

video = pafy.new(url)

audio = video.audiostreams

print(f"Avaliable audio streams: {audio}")

webms = filter(lambda a: a.extension == "webm", audio)

print(audio[0].bitrate)

l = float("inf")
choice = None
for webm in webms:
    b = float(webm.bitrate[:-1])
    if b < l:
        choice = webm
        l = b

print(F"selected {choice}")

choice.download()
transcript = process(choice.filename)
# os.remove(choice.filename)
process_sentence_block(choice.filename, *transcript)
