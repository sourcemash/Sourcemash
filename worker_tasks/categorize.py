import sys
import operator

import logging

from collections import Counter, defaultdict
from string import punctuation
from datetime import datetime, timedelta

import requests
import urllib
import json
from bs4 import BeautifulSoup

import igraph

NGRAMS = 3
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

logger = logging.getLogger('Sourcemash')

class Categorizer:

    def __init__(self):
        self.memoized_related_articles = defaultdict(set)
        self.memoized_article_links = defaultdict(set)
        self.memoized_semantic_relatedness_scores = defaultdict(lambda: defaultdict(float))


    def categorize_item(self, title, text):
        # Extract words present in category dictonary
        keyword_candidates = self.get_keyword_candidates(title, text)
        self.memoize_related_articles(dict(keyword_candidates).keys())
        self.memoize_article_links(dict(keyword_candidates).keys())
        assigned_articles = self.assign_closest_articles(dict(keyword_candidates).keys())
        semantic_graph = self.build_semantic_graph(assigned_articles)
        communities = semantic_graph.community_multilevel(weights='weight')
        selected_categories = self.get_best_keywords(communities, keyword_candidates)

        return selected_categories


    def get_keyword_candidates(self, title, text):
        title_ngrams = self.get_valid_ngrams(title)
        text_ngrams = self.get_valid_ngrams(text)

        # Apply Weights
        for ngram, count in text_ngrams.iteritems():
            # From Title
            if ngram in title_ngrams:
                text_ngrams.update({ngram: count})

            # Bigram or Trigram
            for gram in range(ngram.count(' ')):
                text_ngrams.update({ngram: count})

        return (title_ngrams + text_ngrams).most_common(30)


    def get_valid_ngrams(self, string):
        ngrams = Counter()

        split_words = [word.strip(punctuation).replace(u"\u2018", "").replace(u"\u2019", "").replace(u"\u201c","").replace(u"\u201d", "") for word in string.split()]

        marked_for_deletion = []
        for index, word in enumerate(split_words):
            try:
                decoded = word.decode('utf-8', errors='replace')      
                split_words[index] = decoded
            except UnicodeEncodeError:
                marked_for_deletion.append(word)

        for word in marked_for_deletion:
            split_words.remove(word)

        for n in range(NGRAMS):
            ngrams_tupled = zip(*[split_words[i:] for i in range(n + 1)])
            ngrams_stringed = [' '.join(word) for word in ngrams_tupled]

            for ngram in ngrams_stringed:
                if self.is_viable_candidate(ngram):
                    ngrams.update([ngram])

        return ngrams

    def memoize_related_articles(self, ngrams):
        """
        Store all related (disambiguated) Wiki articles for each
        ngram, if missing from memoization
        """
        logger.debug("Memoizing Related Articles...")

        # Scrape for disambiguation links
        disambiguated_titles = map(lambda x: x + " (disambiguation)", ngrams)
        self._scrape_wiki_links(disambiguated_titles)

        # Scrape for remaining disambiguation pages 
        # without (disambiguation) in title. If neither, assign own page title.
        self._scrape_wiki_links(ngrams)

    def memoize_article_links(self, ngrams):

        logger.debug("\nMemoizing Articles Links...")

        article_titles = []
        for ngram in ngrams:
            related_articles = self.memoized_related_articles[ngram]
            if related_articles:
                article_titles += related_articles

        self._scrape_wiki_links(article_titles)


    def assign_closest_articles(self, ngrams):
        assigned_articles = defaultdict(list)

        logger.debug("\nAssigning Articles to Phrases...")

        ngrams = filter(lambda x: self.memoized_related_articles[x], ngrams)

        # First assign all of the definite matches
        for ngram in ngrams:            
            if len(self.memoized_related_articles[ngram]) == 1:
                assigned_articles[next(iter(self.memoized_related_articles[ngram]))].append(ngram)

        # Generate context links from definite matches
        context_links = Counter()
        for assigned_article in assigned_articles:
            context_links.update(self.memoized_article_links[assigned_article])

        # Word-Sense Disambiguate on remaining words, using context links
        for ngram in ngrams:
            # We already checked for length of 1 above, and
            # we can discard any terms with no related articles
            if len(self.memoized_related_articles[ngram]) < 2:
                continue

            max_relatedness_score = 0
            best_article = None
            for article in self.memoized_related_articles[ngram]:

                if not self.memoized_article_links[article]:
                    continue

                article_relatedness_total = 0

                for link in context_links:
                    weight = 1
                    if "Template" in link or \
                        "Wikipedia" in link or \
                        "Help" in link:
                        weight = 0.1
                    if "Category" in link:
                        weight = 1.5
                    if link == article:
                        weight = 2

                    if link in self.memoized_article_links[article] or link == article:
                        article_relatedness_total += (weight * context_links[link])

                article_relatedness_score = 2.0 * article_relatedness_total / (len(self.memoized_article_links[article]) + len(context_links))

                if article_relatedness_score > max_relatedness_score:
                    max_relatedness_score = article_relatedness_score
                    best_article = article

            if best_article:
                assigned_articles[best_article].append(ngram)

        return assigned_articles


    def build_semantic_graph(self, articles):
        logger.debug("\nBuilding semantic graph...")

        edges = []
        vertex_attrs = {"name": []}
        edge_attrs = {"weight": []}

        for i, article in enumerate(articles):
            vertex_attrs["name"].append(article)

            weight = len(articles[article])

            for j, compared_article in enumerate(articles):
                if i == j:
                    continue

                if not self.memoized_article_links[article] or not self.memoized_article_links[compared_article]:
                    continue

                edge_weight = weight * self.get_relatedness_score(article, compared_article)

                if edge_weight:
                    edges.append([i, j])
                    edge_attrs["weight"].append(edge_weight)

        return igraph.Graph(edges=edges, vertex_attrs=vertex_attrs, edge_attrs=edge_attrs)

    def get_relatedness_score(self, article_1, article_2):

        if article_1 in self.memoized_semantic_relatedness_scores:
            if article_2 in self.memoized_semantic_relatedness_scores[article_1]:
                return self.memoized_semantic_relatedness_scores[article_1][article_2]

        article_1_links = self.memoized_article_links[article_1]
        article_2_links = self.memoized_article_links[article_2]

        overlapping_links_count = 0

        for article_link in article_1_links:
            weight = 1
            if "Template" in article_link or \
                "Wikipedia" in article_link or \
                "Help" in article_link:
                weight = 0.1
            if "Category" in article_link:
                weight = 1.5
            if article_link == article_2:
                weight = 2

            if article_link in article_2_links or article_link == article_2:
                overlapping_links_count += weight

        total_links_count = len(article_1_links) + len(article_2_links)

        semantic_relatedness_score = 2.0 * overlapping_links_count / total_links_count

        self.memoized_semantic_relatedness_scores[article_1][article_2] = semantic_relatedness_score
        self.memoized_semantic_relatedness_scores[article_2][article_1] = semantic_relatedness_score

        return semantic_relatedness_score


    def get_best_keywords(self, communities, original_keywords):
        clusters = {}

        keyword_counts = dict(original_keywords)

        for cluster in communities.subgraphs():
            vertex_names = map(lambda x: x['name'], cluster.vs)
            
            total_vertices = len(vertex_names)
            matching_vertices_count = sum(map(lambda x: keyword_counts[x] if x in keyword_counts else 0, vertex_names))

            clusters[tuple(vertex_names)] = float(matching_vertices_count) / total_vertices

        clusters = sorted(clusters.items(), key=operator.itemgetter(1), reverse=True)

        logger.debug(clusters)

        best_keywords = Counter()
        for cluster in clusters:
            if cluster[1] > 1:
                for keyword in cluster[0]:
                    best_keywords.update({keyword: keyword_counts[keyword] if keyword in keyword_counts else 0})

        if 0 < len(best_keywords) < 2:
            best_keywords.update({original_keywords[0][0]: original_keywords[0][1]})
            best_keywords.update({original_keywords[1][0]: original_keywords[1][1]})
        
        # TODO: Skip nested categories

        return map(lambda x: x[0].title(), best_keywords.most_common())


    def is_viable_candidate(self, phrase):
        # Ignore 1-character phrases
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

        # Ignore non-titled ngrams
        if len(words) == 2 and not phrase.istitle():
            return False

        if len(words) == 3:
            if words[2].lower() in STOP_WORDS:
                return False

            titled_words = map(lambda x: x.istitle(), words)
            if titled_words not in [[True, False, True], [True, True,True]]:
                return False 

        return True

    def _scrape_wiki_links(self, titles):
        unscraped_titles = filter(lambda x: x not in self.memoized_article_links and x not in self.memoized_related_articles, titles)

        if not unscraped_titles:
            return

        total_titles = len(unscraped_titles)
        for i in xrange(0, len(unscraped_titles), 5):
            logger.debug("\r%d%%" % (100 * i / total_titles))
            sys.stdout.flush()

            title_chunk = unscraped_titles[i:i + 5]

            joined_titles = "|".join(title_chunk)

            resp = requests.get(WIKIPEDIA_LINKS % urllib.quote(joined_titles))
            data = json.loads(resp.text, object_hook=self._decode_dict)

            sublinks = self._compile_sublinks(data['query'])

            links = defaultdict(set)
            disambiguation_pages = set()
            for page in data['query']['pages'].itervalues():

                if "missing" in page:
                    self.memoized_article_links[page['title']] = None
                    self.memoized_related_articles[page['title']] = None
                    continue

                if 'pageprops' in page and ('disambiguation' in page['title'] or 'disambiguation' in page['pageprops']):
                    disambiguation_pages.add(page['title'])

                if "links" in page:
                    for link in page['links']:
                        links[page["title"]].add(link['title'])

            while 'continue' in data:
                continue_param = "&plcontinue=" + data['continue']['plcontinue']
                resp = requests.get(WIKIPEDIA_LINKS % (urllib.quote(joined_titles) + continue_param))
                data = json.loads(resp.text, object_hook=self._decode_dict)

                sublinks = self._compile_sublinks(data['query'], sublinks)

                for page in data['query']['pages'].itervalues():

                    if "missing" in page:
                        continue

                    if 'pageprops' in page and ('disambiguation' in page['title'] or 'disambiguation' in page['pageprops']):
                        disambiguation_pages.add(page['title'])

                    if "links" in page:
                        for link in page['links']:
                            links[page["title"]].add(link['title'])

            for link_title in links:
                # Store links in article
                if link_title not in self.memoized_article_links:
                    self.memoized_article_links[link_title] = links[link_title]

                if link_title in sublinks:
                    for sublink in sublinks[link_title]:
                        if sublink not in self.memoized_article_links:
                            self.memoized_article_links[sublink] = links[link_title]

                # Store related articles
                if link_title in disambiguation_pages:
                    related_links = filter(lambda x: link_title.replace(" (disambiguation)", "").lower() in x.lower(), links[link_title])

                    if link_title not in self.memoized_related_articles:
                            self.memoized_related_articles[link_title] = related_links
                            self.memoized_related_articles[link_title.replace(" (disambiguation)", "")] = related_links


                    if link_title in sublinks:
                        for sublink in sublinks[link_title]:
                            if sublink not in self.memoized_related_articles:
                                self.memoized_related_articles[sublink] = related_links
                                self.memoized_related_articles[sublink.replace(" (disambiguation)", "")] = related_links
                else:
                    if link_title not in self.memoized_related_articles:
                            self.memoized_related_articles[link_title] = set([link_title])

                    if link_title in sublinks:
                        for sublink in sublinks[link_title]:
                            if sublink not in self.memoized_related_articles:
                                self.memoized_related_articles[sublink] = set([link_title])


    def _compile_sublinks(self, data, link_path=None):
        """Flatten normalized and redirect links for quick lookup"""

        link_redirects = defaultdict(set)
        if "redirects" in data:
            for redirect in data['redirects']:
                link_redirects[redirect['to']].add(redirect['from'])

        normalized_links = {}
        if "normalized" in data: 
            for normalized_link in data['normalized']:
                normalized_links[normalized_link['to']] = normalized_link['from']

        if not link_path:
            link_path = link_redirects    

        for normalized_link_to, normalized_link_from in normalized_links.iteritems():
            link_path[normalized_link_to].add(normalized_link_from)
            for to_link, from_links in link_path.iteritems():
                if normalized_link_to in from_links:
                    link_path[to_link].update(normalized_link_to, normalized_link_from)
                    break

        return link_path

    def _decode_list(self, data):
        rv = []
        for item in data:
            if isinstance(item, unicode):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = self._decode_list(item)
            elif isinstance(item, dict):
                item = self._decode_dict(item)
            rv.append(item)
        return rv

    def _decode_dict(self, data):
        rv = {}
        for key, value in data.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = self._decode_list(value)
            elif isinstance(value, dict):
                value = self._decode_dict(value)
            rv[key] = value
        return rv


if __name__ == "__main__":
    categorizer = Categorizer()
    # print categorizer.categorize_item("Officials Say Ebola Cases Are Falling In West Africa", "")
    print categorizer.categorize_item("Officials Say Ebola Cases Are Falling In West Africa", "GENEVA The number of people falling victim to the Ebola virus in West Africa has dropped to the lowest level in months, the World Health Organization said on Friday, but dwindling funds and a looming rainy season threaten to hamper efforts to control the disease. More than 8,668 people have died in the Ebola epidemic in West Africa, which first surfaced in Guinea more than a year ago. But the three worst-affected countries Guinea, Liberia and Sierra Leone have now recorded falling numbers of new cases for four successive weeks, Dr. Bruce Aylward, the health organizations assistant director general, told reporters in Geneva. Liberia, which was struggling with more than 300 new cases a week in August and September, recorded only eight new cases in the week to Jan. 18, the organization reported. In Sierra Leone, where the infection rate is now highest, there were 118 new cases reported in that week, compared with 184 in the previous week and 248 in the week before that. Speaking just after a visit to the region, Dr. Aylward said on Friday that the really substantial reduction in new cases was a direct result of last falls vast buildup of resources for fighting the epidemic. This is the first time that the countries were in a position to stop Ebola, he said. President Ernest Bai Koroma of Sierra Leone announced on Friday that the country was lifting the travel restrictions that it had imposed in an effort to contain the virus. Victory is in sight, Mr. Koroma said. Dr. Aylward cautioned that the things that have been driving the reduction so far will not get us to zero, and that health authorities do not yet have the spread of the disease completely under control. The good news about falling infection rates also bore a danger, Dr. Aylward said: Pledges of international financial support for the Ebola response were falling, as well. He said that $1.5 billion was needed to fight the disease for the next six months, but that only $482 million had been committed so far. Most of those pledges were made last year.'")