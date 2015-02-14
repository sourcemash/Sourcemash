import pytest
from sourcemash.categorize import Categorizer
from collections import Counter

class TestCategorize:

    def test_categorize_item(self):
        categorizer = Categorizer()

        title = "Officials Say Ebola Cases Are Falling In West Africa"
        text = "GENEVA The number of people falling victim to the Ebola virus in West Africa has dropped to the lowest level in months, the World Health Organization said on Friday, but dwindling funds and a looming rainy season threaten to hamper efforts to control the disease. More than 8,668 people have died in the Ebola epidemic in West Africa, which first surfaced in Guinea more than a year ago. But the three worst-affected countries Guinea, Liberia and Sierra Leone have now recorded falling numbers of new cases for four successive weeks, Dr. Bruce Aylward, the health organizations assistant director general, told reporters in Geneva. Liberia, which was struggling with more than 300 new cases a week in August and September, recorded only eight new cases in the week to Jan. 18, the organization reported. In Sierra Leone, where the infection rate is now highest, there were 118 new cases reported in that week, compared with 184 in the previous week and 248 in the week before that. Speaking just after a visit to the region, Dr. Aylward said on Friday that the really substantial reduction in new cases was a direct result of last falls vast buildup of resources for fighting the epidemic. This is the first time that the countries were in a position to stop Ebola, he said. President Ernest Bai Koroma of Sierra Leone announced on Friday that the country was lifting the travel restrictions that it had imposed in an effort to contain the virus. Victory is in sight, Mr. Koroma said. Dr. Aylward cautioned that the things that have been driving the reduction so far will not get us to zero, and that health authorities do not yet have the spread of the disease completely under control. The good news about falling infection rates also bore a danger, Dr. Aylward said: Pledges of international financial support for the Ebola response were falling, as well. He said that $1.5 billion was needed to fight the disease for the next six months, but that only $482 million had been committed so far. Most of those pledges were made last year.'"

        categorizer.parse_title_categories([title])
        
        (cat1, cat2) = categorizer.categorize_item(title, text)

        assert (cat1, cat2) == ("Ebola", "West")

    
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