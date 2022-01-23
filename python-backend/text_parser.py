
from typing import Tuple
from pandas import cut
from rake_nltk import Rake
import wikipedia_search
import concurrent.futures

from dataclasses import dataclass


@dataclass
class Fact:
    keyword: str
    description: str
    facts: list[Tuple[str, str]]


videos = {}


def poll_facts(videoname: str, timestamp: float):
    v = videos.get(videoname, None)
    if v == None:
        return None

    for ((t_s, t_e), fact) in v:
        if t_s < timestamp and timestamp < t_e:
            return fact

    return None


def process_sentence_block(videoname: str,  transcript: str, timestamps: list[Tuple[str, float, float]]):
    '''call this one to input data'''

    transcript = transcript.lower()
    timestamps = [(word.lower(), start, end) for word, start, end in timestamps]

    # sentances = [a[0] for a in sentances_timestamped]

    # sentances_l = [x.lower() for x in sentances]

    # Uses stopwords for english from NLTK, and all puntuation characters by
    # default
    r = Rake()

    # Extraction given the text.
    # r.extract_keywords_from_text(incorrect)

    # Extraction given the list of strings where each string is a sentence.
    r.extract_keywords_from_text(transcript)

    cutoff = len(timestamps) ** 0.3

    print(cutoff)

    args1 = []
    args2 = []

    phrase_to_timestamp = {}

    for (score, phrase) in r.get_ranked_phrases_with_scores():
        if score < cutoff:
            continue

        print(score, phrase)

        split = phrase.split(" ")

        valid = False
        p = 0

        cs = 0

        for word, start, end in timestamps:
            if word == split[p]:

                if p == 0:
                    cs = start

                p += 1

                if p == len(split):
                    phrase_to_timestamp[phrase] = (cs, end)
                    valid = True
                    p = 0
            else:
                p = 0

        if valid:
            args1.append(phrase)

            args2.append(wikipedia_search.get_words(phrase))

    print(phrase_to_timestamp)

    timestampedData = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for (phrase, s, r) in executor.map(wikipedia_search.SearchPhrase, args1, args2):
            if phrase == None:
                continue

            timestampedData.append((phrase_to_timestamp[phrase], Fact(phrase, s, r)))

            print("")

            print(phrase)

            print("-------")

            print(s)

            print("---------")

            for k, v in r.items():
                print(f"{k} |  {v}")

            print("-------")

            print(" ")

    videos[videoname] = timestampedData


if __name__ == "__main__":
    import pprint
    incorrect = """Nelson Mandella died in 2006, when he was hit by a bus.
        This caused the current US president, barak obama, to hold a day of mourning"""

    words = incorrect.replace(".", " ")
    words = words.replace(",", " ")
    words = words.split(" ")
    words = [(word, i, i+1) for i, word in enumerate(words)]

    process_sentence_block("video_test", incorrect, words)

    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(videos)

    pp.pprint(poll_facts("video_test", 1.5))
    pp.pprint(poll_facts("video_test", 5))
