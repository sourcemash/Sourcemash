from collections import Counter

def categorizeItem(title, text, category_dict):
	cat1 = ""
	cat2 = ""

	categories = Counter()

	title = title.split()
	text = text.split()

	# Get word counts from title, text of article
	for source in [title, text]:
		for word in source:
			word = word.strip()
			if word in category_dict:
				categories.update([word])

	# Give weights to categories found in title
	for word in title:
		word = word.strip()
		if word in category_dict:
			categories[word] *= 2

	# Return top 2 words in categories
	most_frequent = categories.most_common(2)

	return (most_frequent[0][0], most_frequent[1][0])