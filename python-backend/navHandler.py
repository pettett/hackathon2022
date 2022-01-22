import re
import unicodedata
import os

def SanatiseFileName(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

async def navHandler(url):
    # check if is valid YouTube url
    valid = re.search("http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?", url)
    if not valid:
        return
    
    currentdirname = os.path.dirname(__file__)
    filename = SanatiseFileName(url)
    print(currentdirname)
    print(filename)
    dirpath = os.path.join(currentdirname,'data',filename)
    if os.path.isdir(dirpath):
        print("Already found")
        #TODO: ADD LOGIC
    else:
        os.mkdir(dirpath)


