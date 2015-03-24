# -*- coding: UTF-8 -*-

import pytest

class TestCategorize:

    def test_categorize_item(self, categorizer, ebolaItem):
        categories = categorizer.categorize_item(ebolaItem.title, ebolaItem.text)
        overlapping_categories = filter(lambda x: "Ebola" in x or "West Africa" in x, categories)
        assert len(overlapping_categories) == 2

    def test_categorize_items_too_few_wiki_links(self, categorizer, ebolaItem):
        assert set(categorizer.categorize_item("ZenPayroll", "company")) == set(["Zenpayroll", "Company"])

    def test_empty_categories(self, categorizer):
        categories = categorizer.categorize_item("Of The", "Of The Of The Of The Of The")
        assert categories == [""]

    def test_get_valid_ngrams_apostrophe_s(self, categorizer):
        assert categorizer._get_valid_ngrams("Harry's").keys() == ["Harry"]

    def test_get_valid_ngrams_punctuation(self, categorizer):
        assert categorizer._get_valid_ngrams('Google.').keys() == ["Google"]

    def test_get_valid_ngrams_bigram(self, categorizer):
        assert set(categorizer._get_valid_ngrams("Google Maps")) == set(["Google", "Maps", "Google Maps"])

    def test_is_viable_candidate_single_char(self, categorizer):
        assert categorizer._is_viable_candidate("a") == False

    def test_is_viable_candidate_stopword(self, categorizer):
        assert categorizer._is_viable_candidate("and") == False

    def test_is_viable_candidate_number(self, categorizer):
        assert categorizer._is_viable_candidate("100") == False

    def test_is_viable_candidate_bigram_both_valid(self, categorizer):
        assert categorizer._is_viable_candidate("elemental alligator") == True

    def test_is_viable_candidate_bigram_one_invalid(self, categorizer):
        assert categorizer._is_viable_candidate("and alligator") == False

    def test_is_viable_candidate_trigram_valid(self, categorizer):
        assert categorizer._is_viable_candidate("Abercrombie and Fitch") == True

    def test_decode_list_unicode(self, categorizer):
        assert categorizer._decode_list([u"éxit"]) == ["éxit"]

    def test_decode_list_list(self, categorizer):
        assert categorizer._decode_list([["String", u"éxit"]]) == [["String", "éxit"]]
