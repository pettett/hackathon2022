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
import pandas as pd

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"
WIKIDATA = "https://www.wikidata.org/w/api.php"
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


def get_wikidata_properties_for_id(id: str):
    PARAMS = {
        "format": "json",
        "action": "wbgetclaims",
        "entity": id
    }

    R = S.get(url=WIKIDATA, params=PARAMS)

    d = R.json()["claims"]

    pp.pprint(d["P570"])

    ps = list(d.keys())

    chunksize = 30

    properties = pd.DataFrame(index=d.keys(), columns=["value", "type", "label"])

    properties["type"] = properties.index.map(lambda x: d[x][0]["mainsnak"]["datatype"])
    properties["value"] = properties.index.map(lambda x: d[x][0]["mainsnak"]["datavalue"]["value"])

    for i in range(0, len(ps), chunksize):
        # request properties in chunks of 30
        props = "|".join(ps[i:min(i+chunksize, len(ps))])

        PARAMS = {
            "format": "json",
            "action": "wbgetentities",
            "languages": "en",
            "ids": props,
            "props": "labels",
        }

        PROPS = S.get(url=WIKIDATA, params=PARAMS).json()["entities"]

        for (k, v) in PROPS.items():
            properties["label"][k] = v["labels"]["en"]["value"]

    return properties


wikidata_conversions = {
    "die": "death"


}


def SearchPhrase(phrase):

    # SEARCHPAGE = phrase

    results = wikipedia.search(phrase, results=1)

    r = results[0]

    # Get summary infmation
    summary = wikipedia.summary(r, sentences=3)

    # page = wikipedia.page(r)

    # print(page.__dict__)

    # Get isolated facts about the topic

    id = get_wikidata_id_for_title(r)

    print(get_wikidata_properties_for_id(id))

    data = client.get(id, load=True)

    words = phrase.split(" ")

    # words = [WordNetLemmatizer().lemmatize(word, 'v') for word in words]

    # words = [wikidata_conversions.get(w, w) for w in words]

    print(words)

    for prop in data:

        label = '{!r}'.format(prop.label)[2:-1].split(" ")

        for word in words:
            if word in label:
                print(f"Relevant?: {prop.label}, {data.getlist(prop)}")

    return summary


if __name__ == "__main__":
    SearchPhrase("nelson mandella death")
