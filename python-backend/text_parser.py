
import json
import os
from typing import Tuple
from pandas import cut
from rake_nltk import Rake
import wikipedia_search
import concurrent.futures
import pprint
import utils.file

from utils.json import EnhancedJSONEncoder

from nltk import ConcordanceIndex

from nltk.tokenize import wordpunct_tokenize


class ConcordanceIndex2(ConcordanceIndex):
    def create_concordance(self, word, token_width=13):
        "Returns a list of contexts for @word with a context <= @token_width"
        half_width = token_width // 2
        contexts = []
        for i, token in enumerate(self._tokens):
            if token == word:
                start = i - half_width if i >= half_width else 0
                context = self._tokens[start:i + half_width + 1]
                contexts.append(context)
        return contexts


pp = pprint.PrettyPrinter(indent=1)
videos = {}


def poll_facts(videoname: str, timestamp: float):
    v = videos.get(videoname, None)
    if v == None:
        try:
            with open(os.path.join(utils.file.get_data_dir(), videoname, "facts.json"), "r") as f:
                v = json.loads(f.read())
                if v == None:
                    return None
        except FileNotFoundError:
            return None

    minFact = None
    minTime = 99999999999999

    for ((t_s, t_e), fact) in v:
        if t_s < timestamp:
            if(timestamp - t_s < minTime):
                minFact = fact
                minTime = timestamp - t_s
    return minFact


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

    tokens = wordpunct_tokenize(transcript)

    c = ConcordanceIndex2(tokens)

    phrase_to_timestamp = {}

    for (score, phrase) in r.get_ranked_phrases_with_scores():
        if score < cutoff:
            continue

        print(score, phrase)

        split = phrase.split(" ")

        valid = False
        p = 0

        cs = 0

        related = []

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

            words = phrase.split(" ")
            allWords = set(words)

            for word in words:
                allWords.update(*c.create_concordance(word))

            words = wikipedia_search.get_words(allWords)

            args2.append(words)

    print(phrase_to_timestamp)

    timestampedData = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for (phrase, fact) in executor.map(wikipedia_search.SearchPhrase, args1, args2):
            if phrase == None:
                continue

            #title = wikipedia_search.SearchForTitle(phrase,wikipedia_search.get_words(phrase))

            timestampedData.append((phrase_to_timestamp[phrase], fact))
            # timestampedData.append((phrase_to_timestamp[phrase],Fact(title,s,r)))

            pp.pprint(fact)

    print(f"Finished getting wikipedia data for {videoname}")
    videos[videoname] = timestampedData
    path = os.path.join(utils.file.get_data_dir(), videoname, "facts.json")
    with open(path, "w") as f:
        f.write(json.dumps(timestampedData, cls=EnhancedJSONEncoder))


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
