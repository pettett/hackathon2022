from importlib.resources import path
import pafy
from deepgram_test import *
from text_parser import *
import os
import utils.file

def parse_video(url, videoname):
    video = pafy.new(url)

    audio = video.audiostreams
    choice = audio[0]

    filepath = os.path.join(utils.file.get_data_dir, videoname)
    for a in audio:
        if(a.get_filesize() < choice.get_filesize()):
            choice = a
    choice.download(file=filepath)
    transcript = process(choice.filename)
    #os.remove(choice.filename)
    process_sentence_block(videoname, *transcript)


