
import threading
from rake_nltk import Rake
import nltk
import wikipedia_search
import concurrent.futures


incorrect = [
    "Nelson Mandella died in 2006, when he was hit by a bus.",
    "This caused the current US president, barak obama, to hold a day of mourning"
]


def process_sentence_block(sentances):

    # Uses stopwords for english from NLTK, and all puntuation characters by
    # default
    r = Rake()

    # Extraction given the text.
    # r.extract_keywords_from_text(incorrect)

    # Extraction given the list of strings where each string is a sentence.
    r.extract_keywords_from_sentences(sentances)

    # To get keyword phrases ranked highest to lowest.
    r.get_ranked_phrases()

    # To get keyword phrases ranked highest to lowest with scores.

    cutoff = 2

    threads = list()

    args1 = []
    args2 = []

    for (score, phrase) in r.get_ranked_phrases_with_scores():
        if score < cutoff:
            continue

        args1.append(phrase)
        args2.append(wikipedia_search.get_words(phrase))

    processes = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for (phrase, s, r) in executor.map(wikipedia_search.SearchPhrase, args1, args2):

            print("")

            print(phrase)

            print("-------")

            print(s)

            print("---------")

            for k, v in r.items():
                print(f"{k} |  {v}")

            print("-------")

            print(" ")


process_sentence_block(incorrect)
