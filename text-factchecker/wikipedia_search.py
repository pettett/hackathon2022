#!/usr/bin/python3

"""
    search.py

    MediaWiki API Demos
    Demo of `Search` module: Search for a text or title

    MIT License
"""
import re
import requests
import wikipedia
from wikidata.client import Client
from nltk.stem.wordnet import WordNetLemmatizer
import pprint

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"
client = Client()

pp = pprint.PrettyPrinter(indent=1)


def trim_html(text: str):
    return re.sub("<.*?>", "", text)


def get_wikidata_id_for_title(title: str):
    PARAMS = {
        "action": "query",
        "format": "json",
        "prop": "pageprops",
        "titles": title,
    }

    R = S.get(url=URL, params=PARAMS)

    return R.text.split('wikibase_item":"')[1].split('"')[0]


wikidata_conversions = {
    "die": "death"
}


def SearchPhrase(phrase):

    # SEARCHPAGE = phrase

    results = wikipedia.search(phrase, results=1)

    r = results[0]

    # Get summary infmation
    summary = wikipedia.summary(r, sentences=3)

    #page = wikipedia.page(r)

    # print(page.__dict__)

    # Get isolated facts about the topic

    id = get_wikidata_id_for_title(r)

    data = client.get(id, load=True)

    words = [WordNetLemmatizer().lemmatize(word, 'v') for word in phrase.split(" ")]

    words = [wikidata_conversions.get(w, w) for w in words]

    # print(words)

    for prop in data:

        label = '{!r}'.format(prop.label).split(" ")

        for word in words:
            if word in label:
                print(f"Relevant?: {prop.label}, {data.getlist(prop)}")
                break

        else:
            print(f"nothing for {label}")

    return summary


if __name__ == "__main__":
    SearchPhrase("nelson mandella died")
