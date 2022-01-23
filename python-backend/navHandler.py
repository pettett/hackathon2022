import re
import os

import utils.file
import videodownload


def url_to_identifier(url):
    # check if is valid YouTube url
    if (url[:32] == "https://www.youtube.com/watch?v=") and (len(url) == 43):
        return utils.file.sanatise_file_name(url)
    raise ValueError("Invalid url")


async def nav_handler(url):
    try:
        filename = url_to_identifier(url)
    except ValueError as e:
        print(e)
        print("idiot")
        return
    print(filename)
    print("bob ross")
    dirpath = os.path.join(utils.file.get_data_dir(), filename)

    if os.path.isdir(dirpath):
        print("Already found")
        return
        # TODO: ADD LOGIC
    else:
         os.mkdir(dirpath)
    await videodownload.parse_video(url, filename)
