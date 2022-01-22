
from rake_nltk import Rake
import nltk
from wikipedia_search import SearchPhrase


# Reguires:

# nltk.download('omw-1.4')
# nltk.download('stopwords')
# nltk.download('wordnet')


incorrect = [
    "Nelson Mandella died in 2006, when he was hit by a bus",
    "This caused the current US president, barak obama, to hold a day of mourning"
]


# Uses stopwords for english from NLTK, and all puntuation characters by
# default
r = Rake()

# Extraction given the text.
# r.extract_keywords_from_text(incorrect)

# Extraction given the list of strings where each string is a sentence.
r.extract_keywords_from_sentences(incorrect)

# To get keyword phrases ranked highest to lowest.
r.get_ranked_phrases()

# To get keyword phrases ranked highest to lowest with scores.

cutoff = 2


for (score, phrase) in r.get_ranked_phrases_with_scores():
    if score < cutoff:
        continue

    data = SearchPhrase(phrase)

    print(f"""||| {phrase} |||:,
    
     {data }""")
