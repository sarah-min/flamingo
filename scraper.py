# pip install beautifulsoup4
# pip install requests
from bs4 import BeautifulSoup, Tag, NavigableString
import requests
import re

# used AI to gen this list from the paragraph on wiktionary
PARTS_OF_WORDS = {
    # Parts of speech
    "Adjective", "Adverb", "Ambiposition", "Article", "Circumposition",
    "Classifier", "Conjunction", "Contraction", "Counter", "Determiner",
    "Ideophone", "Interjection", "Noun", "Numeral", "Participle",
    "Particle", "Postposition", "Preposition", "Pronoun",
    "Proper noun", "Verb",

    # Morphemes
    "Circumfix", "Combining form", "Infix", "Interfix",
    "Prefix", "Root", "Suffix",

    # Symbols and characters
    "Diacritical mark", "Letter", "Ligature", "Number",
    "Punctuation mark", "Syllable", "Symbol",

    # Phrases
    "Phrase", "Proverb", "Prepositional phrase",

    # Han characters
    "Han character", "Hanzi", "Kanji", "Hanja",

    # Other
    "Romanization",
    "Logogram",
    "Determinative",
}

# for a singular definition of a word
class Definition:
    def __init__(self, u, d):
        self.usage = u # origin-ish? like AAVE, slang, biology, law. NOT always there
        self.definition = d # straight definition

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Usage: \"{self.usage}\" Definition: \"{self.definition}\""


# for separating word categories (ex. verb, noun)
class KindOfWord:
    def __init__(self, cat, ety, un):
        self.category = cat
        self.etymology = ety
        self.usage_notes = un
        self.definitions = []

    def set_defs(self, defs):
        self.definitions = defs

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Category: {self.category}\nEtymology: {self.etymology}\nUsage notes: {self.usage_notes}\nDefitions: {self.definitions}"

class Word:
    def __init__(self, l, kof):
        self.link = l
        self.kof = kof # list of kind of words

    def __str__(self):
        return f"Link: {self.link}\nKof: {self.kof}"

# word, sentence it is in, definition, usage

"""
Returns definitions in such a format:
"""
def parse_definition(url) -> Word:
    try:
        headers = { "User-Agent": "Flamingo/1.0 (contact: amzhao@usc.edu)" }
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, 'html.parser')
        accepted_languages = tuple("English")
        start = next(item for item in soup.find_all(class_="mw-heading2") 
                     if item.get_text(strip=True).startswith(accepted_languages))
        content = []
        for item in start.find_all_next():
            if "mw-heading2" in item.get('class', []) and not item.get_text(strip=True).startswith(accepted_languages):
                break
            content.append(item)

        headers = []
        for item in content:
            if item.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                headers.append(item)
        kinds: list[KindOfWord] = []
        parts = tuple(PARTS_OF_WORDS)

        for header in headers:
            text = header.text

            if (text.startswith("Etymology")):
                ety = get_clean_text(header.find_next("p"))
                if (ety.startswith("See the etymology") and len(kinds) != 0):
                    ety = kinds[-1].etymology
                kinds.append(KindOfWord(None, ety, None))

            if (text.startswith(parts)):
                cat = text

                if (len(kinds) == 0):
                    kinds.append(KindOfWord(cat, None, None))
                elif (kinds[-1].category != None):
                    kinds.append(KindOfWord(cat, kinds[-1].etymology, None))
                else:
                    kinds[-1].category = cat

                def_list = header.find_next("ol")
                
                for li in def_list.find_all("li",recursive=False):
                    curr_def: str = ""

                    for item in li.children:
                        if isinstance(item, Tag):
                            curr_def += get_clean_text(item)
                        elif isinstance(item, NavigableString):
                            curr_def += str(item)

                    nl = curr_def.find("\n")
                    if (nl != -1):
                        curr_def = curr_def[:nl]
                    if len(curr_def) == 0:
                        continue
                    left = curr_def.find("(")
                    right = curr_def.find(")")

                    usage = ""
                    definition = curr_def

                    if (left != -1 and right != -1):
                        usage = curr_def[left + 1 : right].strip()
                        if right != len(curr_def) - 1:
                            definition = curr_def[right + 1:].strip()
                    
                    kinds[-1].definitions.append(Definition(usage, definition))
                    

            if (text.startswith("Usage notes")):
                un = get_clean_text(header.find_next("ul"))
                kinds[-1].usage_notes = un

        return Word(url, kinds)
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        exit()

def get_clean_text(tag):
    text = tag.get_text(" ", strip=True)
    text = re.sub(r"\s+([.,;:!?\)\]\}]+)", r"\1", text)
    return text

def fetch_link(word):
    return f"https://en.wiktionary.org/wiki/{word}"

#word = parse_definition("https://en.wiktionary.org/wiki/woke")
#print(word)