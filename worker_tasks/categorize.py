from collections import Counter
from string import punctuation
from datetime import datetime, timedelta

from sourcemash.models import Item

TITLE_WORD_WEIGHT = 2
BIGRAM_WEIGHT = 2

STOP_WORDS = [ "a", "about", "above", "above", "across", "after", "afterwards", \
    "again", "against", "all", "almost", "alone", "along", "already", \
    "also","although","always","am","among", "amongst", "amoungst", \
    "amount",  "an", "and", "another", "any","anyhow","anyone","anything",\
    "anyway", "anywhere", "are", "around", "as",  "at", "back","be","became",\
    "because","become","becomes", "becoming", "been", "before", "beforehand", \
    "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", \
    "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", \
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", \
    "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", \
    "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", \
    "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", \
    "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", \
    "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", \
    "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", \
    "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", \
    "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", \
    "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", \
    "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", \
    "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", \
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", \
    "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", \
    "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", \
    "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", \
    "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", \
    "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", \
    "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", \
    "such", "system", "take", "ten", "than", "that", "the", "their", "them", \
    "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", \
    "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", \
    "those", "though", "three", "through", "throughout", "thru", "thus", "to", \
    "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", \
    "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", \
    "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", \
    "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", \
    "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", \
    "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", \
    "yourselves", "the" ] # Source: http://xpo6.com/list-of-english-stop-words/

class Categorizer:

    def __init__(self):
        self.title_categories = Counter()

    def categorize_item(self, title, text):
        categories = Counter()

        # Extract words present in category dictonary
        title = filter(self.is_valid_word, self.polished_string(title))
        text = filter(self.is_valid_word, self.polished_string(text))

        # Get word counts from title, text of article
        categories.update(title + text)

        # Give weights to categories found in title
        for word in title:
            categories[word] *= TITLE_WORD_WEIGHT

        # Give additional weights to bigrams
        for category in categories:
            if isinstance(category, tuple):
                categories[category] *= BIGRAM_WEIGHT

        cat1 = ""
        cat2 = ""

        # Pick top 2 words until categories don't overlap
        for category, count in categories.most_common():
            if str(cat1) in str(cat2):
                cat1 = category
            elif str(cat2) in str(cat1):
                cat2 = category
            else:
                break

        if isinstance(cat1, tuple):
            cat1 = ' '.join(cat1)

        if isinstance(cat2, tuple):
            cat2 = ' '.join(cat2)

        return cat1, cat2


    def reset_title_categories(self):
        self.title_categories.clear()

        one_day_ago = datetime.now() - timedelta(hours=24)
        titles = [item.title for item in Item.query.filter(Item.category_1==None, Item.last_updated>=one_day_ago).all()]
        self.parse_title_categories(titles)


    def parse_title_categories(self, titles):
        for title in titles:
            for word in self.polished_string(title):
                if self.is_valid_word(word):
                    self.title_categories.update([word])


    def polished_string(self, string):
        words = string.replace("'s", '').split()
        
        # Unigrams
        for word in words:
            yield word.strip(punctuation)

        # Bigrams
        for word in zip(*[words[i:] for i in range(2)]):
            yield word


    def is_valid_word(self, word):

        # If bigram, check that both words are valid
        if isinstance(word, tuple):
            return self.is_valid_word(word[0]) and self.is_valid_word(word[1])

        # Ignore single characters
        if len(word) < 2:
            return False

        # Ignore stop words
        if word.lower() in STOP_WORDS:
            return False

        # Ignore numbers
        try:
            float(word)
            return False
        except ValueError:
            pass

        return True