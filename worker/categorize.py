# categorize.py
#
# Adapted from algorithm by Grineva, et. al. presented at:
# http://www.slideshare.net/maria.grineva/extracting-key-terms-from-noisy-and-multitheme-documents?related=1
#
# Algorithm Overview
# 1) Get initial list of possible keyword candidates using ngram frequencies
# 2) For each keyword candidate, use Wikipedia to extract all related article titles
#       a) Related articles are called (disambiguation links) on Wikipedia
# 3) Try to assign one Wikipedia article to each keyword candidate
#       a) First, assign articles to the keywords that have only 1 related article
#           i) i.e. Sergey Brin only corresponds to wikipedia.org/wiki/Sergey_Brin, whereas Apple might be any link in wikipedia.org/wiki/Apple_(disambiguation).
#       b) Use these "auto-assigned" articles as the context to narrow the other categories' article
#       c) With the context from (b), compute relatedness scores to find the best article match
#           i) relatedness score = [SUM OF SHARED WIKIPEDIA HYPERLINKS] / [TOTAL NUMBER OF WIKIPEDIA HYPERLINKS]
# 4) With each keyword assigned 1 article, create a graph where each vertex is an article and the edge weight
#       is the relatedness score between two articles
# 5) Analyze the graph from (4) to identify keyword clusters
# 6) Only keep the clusters that have a sufficient number of keywords that contain an original keyword candidate from (1)
# 8) Return the best keywords
#       a) For now, we still pick the top two keywords by frequency from kept clusters, but...
#       b) TODO: WE WILL KEEP ALL KEYWORDS FROM THE KEPT CLUSTERS


import logging

from collections import Counter, defaultdict
from string import punctuation

import requests
import json

import networkx as nx
import community    # python-louvain

logger = logging.getLogger('Sourcemash')

NGRAMS = 3
MAX_CANDIDATE_COUNT = 20
MINIMUM_RELATEDNESS_SCORE = 0.1
WIKIPEDIA_LINKS = "http://en.wikipedia.org/w/api.php?action=query&prop=pageprops|links&continue=&pllimit=500&redirects&format=json&titles=%s"
WIKIPEDIA_ARTICLE = "http://en.wikipedia.org/wiki/%s"

STOP_WORDS = [ "a", "about", "above", "across", "after", "afterwards", \
    "again", "against", "all", "almost", "alone", "along", "already", \
    "also","although","always","am","among", "amongst", "amoungst", \
    "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything",\
    "anyway", "anywhere", "are", "around", "as",  "at", "back","be","became",\
    "because","become","becomes", "becoming", "been", "before", "beforehand", \
    "behind", "being", "below", "beside", "besides", "between", "beyond", \
    "both", "bottom", "but", "by", "call", "can", "cannot", "can't", "could", \
    "couldn't", "cry", "de", "describe", "detail", "do", "done", "don't", "down", \
    "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", \
    "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", \
    "everywhere", "except", "few", "fifteen", "fify", "fill", "find", \
    "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", \
    "front", "full", "further", "get", "give", "go", "had", "has", "hasn't", "have", \
    "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", \
    "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", \
    "if", "in", "inc", "indeed", "into", "is", "it", "its", "itself", \
    "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", \
    "may", "me", "meanwhile", "might", "mine", "more", "moreover", "most", \
    "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", \
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", \
    "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", \
    "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", \
    "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", \
    "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", \
    "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", \
    "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", \
    "such", "take", "ten", "than", "that", "the", "their", "them", \
    "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", \
    "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", \
    "those", "though", "three", "through", "throughout", "thru", "thus", "to", \
    "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", \
    "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", \
    "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", \
    "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", \
    "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", \
    "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", \
    "yourselves" ] # Source: http://xpo6.com/list-of-english-stop-words/


class Categorizer:

    def __init__(self):
        self._memoized_related_articles = defaultdict(list)
        self._memoized_article_links = defaultdict(list)
        self._memoized_semantic_relatedness_scores = defaultdict(float)

    def categorize_item(self, title, text):
        # Use ngram word count approach to get possible keywords
        keyword_candidates = self._get_keyword_candidates(title, text)

        # Store possible wiki articles and their links
        self._memoize_related_articles(keyword_candidates.keys())
        self._memoize_article_links(keyword_candidates.keys())

        # Assign best article for each possible keyword
        assigned_articles = self._assign_closest_articles(keyword_candidates.keys())

        # Build a graph and identify keyword clusters
        clustering = None

        if len(assigned_articles) > 2:
            semantic_graph = self._build_semantic_graph(assigned_articles)
            clustering = community.best_partition(semantic_graph)

        # Use keywords from best clusters
        selected_categories = self._get_best_keywords(clustering, keyword_candidates)

        return selected_categories

    def _get_keyword_candidates(self, title, text):
        title_ngrams = self._get_valid_ngrams(title)
        text_ngrams = self._get_valid_ngrams(text)

        ngrams = title_ngrams + text_ngrams

        # Apply weights...
        for ngram, count in ngrams.iteritems():

            # ...from title (x2)
            if ngram in title_ngrams:
                ngrams.update({ngram: count})

            # ...from bigram (x2) or trigram (x3)
            for n in range(ngram.count(' ')):
                ngrams.update({ngram: count})

        return dict(ngrams.most_common(MAX_CANDIDATE_COUNT))

    def _get_valid_ngrams(self, string):
        valid_ngrams = Counter()

        words = [self._clean_word(word) for word in string.split()]

        for n in range(NGRAMS):
            ngrams = zip(*[words[i:] for i in range(n + 1)])

            for ngram in ngrams:
                ngram = ' '.join(ngram)
                if self._is_viable_candidate(ngram):
                    valid_ngrams.update([ngram])

        return valid_ngrams

    def _clean_word(self, word):
        # Strip punctuation
        word = word.strip(punctuation)

        # Remove 's
        word = word.replace("'s", "")

        # Remove Smart Quotes
        word = word.replace(u"\u2018", "").replace(u"\u2019", "").replace(u"\u201c","").replace(u"\u201d", "")

        return word

    def _memoize_related_articles(self, ngrams):
        """Store all related (disambiguated) Wikipedia articles for each ngram"""

        logger.debug("Memoizing Related Articles...")

        # Scrape for disambiguation links
        disambiguated_titles = map(lambda x: x + " (disambiguation)", ngrams)
        self._scrape_wiki_links(disambiguated_titles)

        # Scrape for remaining disambiguation pages without (disambiguation) in title
        # If it's just a regular page (i.e. not disambiguation), then the scrape
        # gets the page links anyway.
        self._scrape_wiki_links(ngrams)

    def _memoize_article_links(self, ngrams):
        """Store all links for a Wikipedia article"""

        logger.debug("Memoizing Articles Links...")

        article_titles = [title for ngram in ngrams for title in self._memoized_related_articles[ngram]]
        self._scrape_wiki_links(article_titles)

    def _scrape_wiki_links(self, titles):
        unscraped_titles = filter(lambda x: x not in self._memoized_article_links, titles)

        for i in xrange(0, len(unscraped_titles), 5):

            grouped_titles = unscraped_titles[i:i + 5]
            grouped_titles_string = "|".join(grouped_titles)

            data = {}
            sublinks = []

            links = defaultdict(list)
            disambiguation_pages = []

            # Make calls to the Wikipedia API for batches of articles
            while 'batchcomplete' not in data:

                url = WIKIPEDIA_LINKS % grouped_titles_string
                if 'continue' in data:
                    url += "&plcontinue=" + data['continue']['plcontinue']

                resp = requests.get(url)
                data = json.loads(resp.text)

                sublinks = self._compile_sublinks(data['query'], sublinks)

                for page in data['query']['pages'].itervalues():

                    if "missing" in page:
                        self._memoized_article_links[page['title']] = []
                        self._memoized_related_articles[page['title']] = []
                        continue

                    if 'pageprops' in page and ('disambiguation' in page['title'] or 'disambiguation' in page['pageprops']):
                        disambiguation_pages.append(page['title'])

                    if "links" in page:
                        for link in page['links']:
                            links[page["title"]].append(link['title'])

            # Store the scraped information
            for link_title in links:

                # Store links in article
                if link_title not in self._memoized_article_links:
                    self._memoized_article_links[link_title] = links[link_title]

                if link_title in sublinks:
                    for sublink in sublinks[link_title]:
                        if sublink not in self._memoized_article_links:
                            self._memoized_article_links[sublink] = links[link_title]

                # Store related articles
                if link_title in disambiguation_pages:
                    related_links = filter(lambda x: link_title.replace(" (disambiguation)", "").lower() in x.lower(), links[link_title])

                    if link_title not in self._memoized_related_articles:
                            self._memoized_related_articles[link_title] = related_links
                            self._memoized_related_articles[link_title.replace(" (disambiguation)", "")] = related_links


                    if link_title in sublinks:
                        for sublink in sublinks[link_title]:
                            if sublink not in self._memoized_related_articles:
                                self._memoized_related_articles[sublink] = related_links
                                self._memoized_related_articles[sublink.replace(" (disambiguation)", "")] = related_links
                else:
                    if link_title not in self._memoized_related_articles:
                            self._memoized_related_articles[link_title] = [link_title]

                    if link_title in sublinks:
                        for sublink in sublinks[link_title]:
                            if sublink not in self._memoized_related_articles:
                                self._memoized_related_articles[sublink] = [link_title]

    def _assign_closest_articles(self, ngrams):
        """Extract Wikipedia articles closest to an ngram"""

        logger.debug("Assigning Articles to Phrases...")

        ambiguous_ngrams = filter(lambda x: len(self._memoized_related_articles[x]) > 1, ngrams)
        unambiguous_ngrams = filter(lambda x: len(self._memoized_related_articles[x]) == 1, ngrams)

        # First assign all of the definite matches
        assigned_articles = [self._memoized_related_articles[unambiguous_ngram][0] for unambiguous_ngram in unambiguous_ngrams]

        # Use the definite matches as contextual links
        context_links = [link for article in assigned_articles for link in self._memoized_article_links[article]]

        # Word-Sense disambiguate remaining words, using context links
        for ambiguous_ngram in ambiguous_ngrams:

            max_relatedness_score = MINIMUM_RELATEDNESS_SCORE
            best_article = None

            max_relatedness_score_without_parentheses = 0
            best_article_without_parentheses = None

            for article in self._memoized_related_articles[ambiguous_ngram]:
                article_relatedness_score = self._get_relatedness_score(self._memoized_article_links[article], context_links)

                if article_relatedness_score > max_relatedness_score:
                    max_relatedness_score = article_relatedness_score
                    best_article = article

                # Prefer Wikipedia article titles without parenthesis (e.g. not Home (2015 film))
                if "(" not in article:
                    if article_relatedness_score > max_relatedness_score_without_parentheses:
                            max_relatedness_score_without_parentheses = article_relatedness_score
                            best_article_without_parentheses = article

            if best_article_without_parentheses:
                assigned_articles.append(best_article_without_parentheses)
            elif best_article:
                assigned_articles.append(best_article)

        return assigned_articles

    def _build_semantic_graph(self, articles):
        """
        Create a category graph where each vertex is a Wikipedia article
        and the edges are weighted by relatedness scores (number of overlapping
        links) between each pair.
        """

        logger.debug("Building semantic graph...")

        G = nx.Graph()
        G.add_nodes_from(articles)

        for article_1 in articles:
            for article_2 in articles:
                if article_1 == article_2:
                    continue

                if (article_1, article_2) in self._memoized_semantic_relatedness_scores:
                    relatedness_score = self._memoized_semantic_relatedness_scores[(article_1, article_2)]
                else:
                    relatedness_score = self._get_relatedness_score(self._memoized_article_links[article_1], self._memoized_article_links[article_2])
                    self._memoized_semantic_relatedness_scores[(article_1, article_2)] = relatedness_score
                    self._memoized_semantic_relatedness_scores[(article_2, article_1)] = relatedness_score

                if relatedness_score:
                    G.add_edge(article_1, article_2, weight=relatedness_score)

        return G

    def _get_relatedness_score(self, article_1_links, article_2_links):
        """Calculate overlap of two Wikipedia articles: 2 * [# of shared links] / [total # of links]"""

        total_links_count = len(article_1_links) + len(article_2_links)

        if not total_links_count:
            return 0

        shared_links_count = 0
        for article_link in article_1_links:
            weight = 1
            if "Template" in article_link or \
                "Wikipedia" in article_link or \
                "Help" in article_link:
                weight = 0.0
            if "Category" in article_link:
                weight = 1.5

            if article_link in article_2_links:
                shared_links_count += weight

        return 2.0 * shared_links_count / total_links_count

    def _get_best_keywords(self, communities, original_keywords):
        """
        Return all keywords from clusters that contain a satisfactory number
        of the original keywords. We take ALL clusters above a threshold
        because some articles have two distinct, but important categories. For
        example, an article about Apple building features for the blind
        community should categorize to both Apple and Blindness.
        """

        best_keywords = set()
        keyword_counts = Counter(original_keywords)

        if communities:
            for cluster in set(communities.values()):
                vertex_names = [nodes for nodes in communities.keys() if communities[nodes] == cluster]

                matching_vertices_count = sum(map(lambda x: keyword_counts[x] if x in keyword_counts else 0, vertex_names))

                cluster_score = float(matching_vertices_count) / len(vertex_names)

                if cluster_score > 1:
                    best_keywords.update(vertex_names)

        if len(best_keywords) < 2:
            best_original_keywords = keyword_counts.most_common(2)
            best_keywords.update([keyword[0] for keyword in best_original_keywords])

        return [keyword.title() for keyword in best_keywords]

    def _is_viable_candidate(self, phrase):

        # Ignore 1-character phrases
        phrase = phrase.strip()
        if len(phrase) < 2:
            return False

        # Ignore numbers
        try:
            phrase = phrase.replace(',', '')
            float(phrase)
            return False
        except ValueError:
            pass

        words = phrase.split()

        # Ignore stop words
        if words[0].lower() in STOP_WORDS:
            return False

        # Ignore non-title trigrams
        if len(words) == 3:
            if words[2].lower() in STOP_WORDS:
                return False

            titled_words = map(lambda x: x.istitle(), words)
            if titled_words not in [[True, False, True], [True, True,True]]:
                return False

        return True

    def _compile_sublinks(self, data, link_path=None):
        """Flatten normalized and redirect links for quick lookup"""

        link_redirects = defaultdict(set)
        if "redirects" in data:
            for redirect in data['redirects']:
                link_redirects[redirect['to']].add(redirect['from'])

        if not link_path:
            link_path = link_redirects

        if "normalized" in data:
            for normalized_link in data['normalized']:
                link_path[normalized_link['to']].add(normalized_link['from'])

                for to_link, from_links in link_path.iteritems():
                    if normalized_link['to'] in from_links:
                        link_path[to_link].update(normalized_link['to'], normalized_link['from'])

        return link_path
