#!/usr/bin/python3

"""
    search.py

    MediaWiki API Demos
    Demo of `Search` module: Search for a text or title

    MIT License
"""
import re
from typing import Tuple
import requests
import wikipedia
from wikidata.client import Client
import pprint
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer

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

    ps = list(d.keys())

    chunksize = 30

    properties = pd.DataFrame(index=d.keys(), columns=["value", "type", "label"])

    properties["type"] = properties.index.map(
        lambda x: d[x][0]["mainsnak"]["datatype"]
    )
    properties["value"] = properties.index.map(
        lambda x: d[x][0]["mainsnak"].get("datavalue", {}).get("value", None)
    )

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


def SearchPhrase(phrase: str, words: list[str]) -> Tuple[str, str, dict[str, str]]:
    #print(f"starting {phrase}")
    # SEARCHPAGE = phrase

    words = [wikidata_conversions.get(w, w) for w in words]

    results = wikipedia.search(phrase, results=1)
    # Get summary infmation
    try:
        r = results[0]

        summary = wikipedia.summary(r, sentences=1)

    except Exception:
        return (None, None, None)
    # page = wikipedia.page(r)

    # print(page.__dict__)

    # Get isolated facts about the topic

    id = get_wikidata_id_for_title(r)

    properties = get_wikidata_properties_for_id(id)

    related = {}

    for i in properties.index:
        label = properties["label"][i]
        value = properties["value"][i]

        ls = label.split(" ")
        for w in words:
            if w in ls:
                related[label] = value

    return phrase, summary, related


def get_words(phrase):
    words = phrase.split(" ")

    words = [WordNetLemmatizer().lemmatize(word, 'v') for word in words]

    return words


if __name__ == "__main__":
    print(SearchPhrase("nelson mandella death", ["nelson", "mandella", "death"]))
