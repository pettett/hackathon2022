import re
import os

import utils.file
import videodownload

def url_to_identifier(url):
    # check if is valid YouTube url
    valid = re.search("http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?", url)
    if not valid:
        raise ValueError("Invalid url")

    return utils.file.sanatise_file_name(url)


async def nav_handler(url):
    try:
        filename = url_to_identifier()
    except:
        return
        
    currentdirname = os.path.dirname(__file__)
    dirpath = os.path.join(utils.file.get_data_dir,filename)

    if os.path.isdir(dirpath):
        print("Already found")
        return
        #TODO: ADD LOGIC
    else:
        os.mkdir(dirpath)
        videodownload.parse_video(url, filename)



