from collections import Counter
from string import punctuation

def categorizeItem(title, text, category_dict):
	categories = Counter()

	# Only consider words present in category dictonary
	title = title.split().filter(lambda word: word in category_dict)
	text = text.split().filter(lambda word: word in category_dict)
	title = map(strip(punctuation), title)
	text = map(strip(punctuation), text)

	# Get word counts from title, text of article
	categories.update(title + text)

	# Give weights to categories found in title
	for word in title:
		categories[word] *= 2

	# Return top 2 words in categories
	most_frequent = categories.most_common(2)

	return (most_frequent[0][0], most_frequent[1][0])