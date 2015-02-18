from collections import Counter
from string import punctuation
from datetime import datetime, timedelta

from sourcemash.models import Item

BIGRAM_WEIGHT = 1.75
CAPITALIZED_WORD_WEIGHT = 1.5

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
        title = filter(self.is_from_titles, self.get_valid_ngrams(title))
        text = filter(self.is_from_titles, self.get_valid_ngrams(text))

        # Get word counts from title, text of article
        categories.update(title + text)

        # Add weight to bigrams and capitalized words
        for category in categories:
            if self.is_bigram(category):
                categories[category] *= BIGRAM_WEIGHT

            if category.istitle():
                categories[category] *= CAPITALIZED_WORD_WEIGHT

        return self.get_best_categories(categories)


    def reset_title_categories(self):
        self.title_categories.clear()

        one_day_ago = datetime.now() - timedelta(hours=24)
        titles = [item.title for item in Item.query.filter(Item.category_1==None, Item.last_updated>=one_day_ago).all()]
        self.parse_title_categories(titles)


    def parse_title_categories(self, titles):
        for title in titles:
            self.title_categories.update(self.get_valid_ngrams(title))


    def get_valid_ngrams(self, string):
        unigrams = [word.strip(punctuation) for word in string.replace("'s", '').split()]
        unigrams = filter(None, unigrams)   # Remove empty strings
        
        bigrams = zip(*[unigrams[i:] for i in range(2)])  # tuples
        bigrams = [' '.join(word) for word in bigrams]  # strings
        
        return filter(self.is_valid_category, unigrams + bigrams)


    def get_best_categories(self, categories):
        """
        Choose the two highest-weighted categories that don't share
        a common word. For example, "Just" and "Just Works" should
        not be selected as the two best.
        """
        cat1, cat2 = "", ""
        for category, weights in categories.most_common():
            if cat1 in cat2:
                cat1 = category
            elif cat2 in cat1:
                cat2 = category
            else:
                break

        return cat1.title(), cat2.title()


    def is_from_titles(self, word):
        # Case-Insensitive Comparison
        # since titles are uppercase and body text lowercase
        return word.title() in self.title_categories


    def is_bigram(self, word):
        return " " in word


    def is_valid_category(self, category):

        # If bigram, check that both words are valid
        if self.is_bigram(category):
            category = category.split()
            return self.is_valid_category(category[0]) and self.is_valid_category(category[1])

        # Ignore single characters
        if len(category) < 2:
            return False

        # Ignore stop words
        if category.lower() in STOP_WORDS:
            return False

        # Ignore numbers
        try:
            float(category)
            return False
        except ValueError:
            pass

        return True