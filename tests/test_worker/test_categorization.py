# -*- coding: UTF-8 -*-

import pytest
import community

class TestCategorize:

    def test_categorize_item_through_Wikipedia(self, categorizer, ebolaItem):
        categories = categorizer.categorize_item(ebolaItem.title, ebolaItem.text)
        overlapping_categories = filter(lambda x: "Ebola" in x or "West Africa" in x, categories)
        assert len(overlapping_categories) > 0

    def test_categorize_items_too_few_links(self, categorizer):
        articles = ["ZenPayroll"]
        original_keywords = {"ZenPayroll": 30, "HR": 5, "SaaS": 10}
        assert set(categorizer._get_best_keywords(None, original_keywords)) == set(["Zenpayroll", "Saas"])

    def test_assign_best_article_with_only_parentheses_links(self, categorizer):
        ngrams = ["staples", "officemax"]
        categorizer._memoized_related_articles["staples"] = ["Staples (Company)", "Staples (office supplies)"]
        categorizer._memoized_related_articles["officemax"] = ["OfficeMax (Company)"]
        categorizer._memoized_article_links["Staples (Company)"] = ["company", "supplies", "store"]
        categorizer._memoized_article_links["OfficeMax (Company)"] = ["company", "supplies", "store"]
        categorizer._memoized_article_links["Staples (office supplies)"] = ["pencil", "paperweight"]

        assert set(categorizer._assign_closest_articles(ngrams)) == set(["OfficeMax (Company)", "Staples (Company)"])

    def test_best_keywords_ignores_nested(self, categorizer):
        keywords = categorizer._get_best_keywords(None,
                                                  ['Google', 'Google Maps'])
        assert keywords == ['Google Maps']

    def test_get_valid_ngrams_apostrophe_s(self, categorizer):
        assert categorizer._get_valid_ngrams("Harry's").keys() == ["Harry"]

    def test_get_valid_ngrams_punctuation(self, categorizer):
        assert categorizer._get_valid_ngrams('Google.').keys() == ["Google"]

    def test_get_valid_ngrams_bigram(self, categorizer):
        assert set(categorizer._get_valid_ngrams("Google Maps")) == set(["Google", "Maps", "Google Maps"])

    def test_relatedness_score_missing_links(self, categorizer):
        assert categorizer._get_relatedness_score([], []) == 0

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
