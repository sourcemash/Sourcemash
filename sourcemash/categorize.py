from collections import Counter
from string import punctuation

def categorizeItem(title, text, category_dict):
	cat1 = ""
	cat2 = ""
	categories = Counter()

	# Only consider words present in category dictonary
	title = filter(lambda word: word in category_dict, title.split())
	text = filter(lambda word: word in category_dict, text.split())
	title = [word.strip(punctuation) for word in title]
	text = [word.strip(punctuation) for word in text]

	# Get word counts from title, text of article
	categories.update(title + text)

	# Give weights to categories found in title
	for word in title:
		categories[word] *= 2

	# Return top 2 words in categories
	most_frequent = categories.most_common(2)

	if len(most_frequent) > 0:
		cat1 = most_frequent[0][0]
		if len(most_frequent) > 1:
			cat2 = most_frequent[1][0]

	return cat1, cat2