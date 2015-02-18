import pytest
from worker_tasks.categorize import Categorizer
from collections import Counter

class TestCategorize:

    def test_categorize_item(self, ebolaItem):
        categorizer = Categorizer()
        
        categorizer.parse_title_categories([ebolaItem.title])
        
        (cat1, cat2) = categorizer.categorize_item(ebolaItem.title, ebolaItem.text)

        assert (cat1, cat2) == ("West Africa", "Ebola")

    
    def test_empty_categories(self):
        categorizer = Categorizer()

        (cat1, cat2) = categorizer.categorize_item("Of The", "Of The Of The Of The Of The")

        assert (cat1, cat2) == ("", "")


    def test_parse_title_categories(self, item):
        categorizer = Categorizer()
        categorizer.parse_title_categories([item.title])

        assert categorizer.title_categories['Item'] == 1


    def test_reset_title_categories(self, item):
        categorizer = Categorizer()
        categorizer.parse_title_categories([item.title])

        assert categorizer.title_categories['Item'] == 1

        categorizer.reset_title_categories()

        # Counts should have been set back to zero
        assert categorizer.title_categories['Item'] == 1


    def test_polished_string_apostrophe_s(self):
        categorizer = Categorizer()
        assert categorizer.get_valid_ngrams("Harry's") == ["Harry"]


    def test_get_valid_ngrams_punctuation(self):
        categorizer = Categorizer()
        assert categorizer.get_valid_ngrams('Google.') == ["Google"]


    def test_get_valid_ngrams_bigram(self):
        categorizer = Categorizer()
        assert categorizer.get_valid_ngrams("Google Maps") == ["Google", "Maps", "Google Maps"]


    def test_is_valid_category_single_char(self):
        categorizer = Categorizer()
        assert categorizer.is_valid_category('a') == False


    def test_is_valid_category_stopword(self):
        categorizer = Categorizer()
        assert categorizer.is_valid_category('and') == False


    def test_is_valid_category_number(self):
        categorizer = Categorizer()
        assert categorizer.is_valid_category('100') == False


    def test_is_valid_category_tuple_both_valid(self):
        categorizer = Categorizer()
        assert categorizer.is_valid_category(('elemental alligator')) == True


    def test_is_valid_category_tuple_one_invalid(self):
        categorizer = Categorizer()
        assert categorizer.is_valid_category(('and alligator')) == False