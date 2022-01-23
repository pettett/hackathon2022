import re
import os

import utils.file
import videodownload


def url_to_identifier(url):
    # check if is valid YouTube url
    valid = re.search("http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?", url)
    print(valid)
    print(url)
    if valid == None:
        raise ValueError("Invalid url")

    return utils.file.sanatise_file_name(url)


async def nav_handler(url):
    try:
        filename = url_to_identifier(url)
    except Exception as e:
        print(e)
        print("idiot")
        return
    print(filename)
    print("bob ross")
    dirpath = os.path.join(utils.file.get_data_dir(), filename)

    # if os.path.isdir(dirpath):
    #print("Already found")
    # return
    # TODO: ADD LOGIC
    # else:
    # os.mkdir(dirpath)
    await videodownload.parse_video(url, filename)
