import pytest
import json

from . import TestBase
from tests.factories import item_factories


def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'

class TestItemAPI(TestBase):

    def test_get_item_present(self, test_client, item):
        r = test_client.get('/api/items/%d' % item.id)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['title'] == item.title
        assert data['item']['vote'] == 0

    def test_get_item_missing(self, test_client):
        r = test_client.get('/api/items/%d' % 10)
        check_valid_header_type(r.headers)
        assert r.status_code == 404

    def test_put_item_upvote(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        upvote = dict(vote=1)
        r = test_client.put('/api/items/%d' % item.id, data=upvote)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['voteSum'] == 1

    def test_put_item_downvote(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        downvote = dict(vote=-1)
        r = test_client.put('/api/items/%d' % item.id, data=downvote)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['voteSum'] == -1

    def test_put_multi_upvotes(self, test_client, user_item_upvote):
        self.login(test_client, user_item_upvote.user.email, user_item_upvote.user.password)

        upvote = dict(vote=1)
        r = test_client.put('/api/items/%d' % user_item_upvote.item.id, data=upvote)
        check_valid_header_type(r.headers)
        assert r.status_code == 422

        data = json.loads(r.data)
        assert "already voted" in data['errors']['vote'][0]

    def test_put_upvote_then_downvote(self, test_client, user_item_upvote):
        self.login(test_client, user_item_upvote.user.email, user_item_upvote.user.password)

        downvote = dict(vote=-1)
        r = test_client.put('/api/items/%d' % user_item_upvote.item.id, data=downvote)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['voteSum'] == -1

    def test_put_downvote_then_upvote(self, test_client, user_item_downvote):
        self.login(test_client, user_item_downvote.user.email, user_item_downvote.user.password)

        upvote = dict(vote=1)
        r = test_client.put('/api/items/%d' % user_item_downvote.item.id, data=upvote)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['voteSum'] == 1

    def test_put_multi_downvotes(self, test_client, user_item_downvote):
        self.login(test_client, user_item_downvote.user.email, user_item_downvote.user.password)

        downvote = dict(vote=-1)
        r = test_client.put('/api/items/%d' % user_item_downvote.item.id, data=downvote)
        check_valid_header_type(r.headers)
        assert r.status_code == 422

        data = json.loads(r.data)
        assert "already voted" in data['errors']['vote'][0]

    def test_put_item_too_big_vote(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        original_vote_count = item.voteSum
        too_big_vote = dict(vote=5)

        r = test_client.put('/api/items/%d' % item.id, data=too_big_vote)
        check_valid_header_type(r.headers)
        assert r.status_code == 422

        data = json.loads(r.data)
        assert "Vote may only be" in data['errors']['vote'][0]

    def test_put_item_non_integer_vote(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        non_integer_vote = dict(vote=0.33)
        r = test_client.put('/api/items/%d' % item.id, data=non_integer_vote)
        check_valid_header_type(r.headers)
        assert r.status_code == 400

    def test_put_vote_missing(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        original_vote_count = item.voteSum
        no_vote = dict()

        r = test_client.put('/api/items/%d' % item.id, data=no_vote)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['voteSum'] == original_vote_count

    def test_put_item_missing(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        upvote = dict(vote=1)
        r = test_client.put('/api/items/%d' % (int(item.id+1)), data=upvote)
        check_valid_header_type(r.headers)
        assert r.status_code == 404

    def test_put_item_mark_read(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        read = dict(unread=False)
        r = test_client.put('/api/items/%d' % item.id, data=read)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['unread'] == False

    def test_put_item_mark_unread(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        read = dict(unread=True)
        r = test_client.put('/api/items/%d' % item.id, data=read)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['unread'] == True

    def test_put_item_mark_read_as_unread(self, test_client, user, user_item_read):
        self.login(test_client, user.email, user.password)

        read = dict(unread=True)
        r = test_client.put('/api/items/%d' % user_item_read.item.id, data=read)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['unread'] == True

    def test_put_item_save(self, test_client, user_item):
        self.login(test_client, user_item.user.email, user_item.user.password)

        saved = dict(saved=True)
        r = test_client.put('/api/items/%d' % user_item.item.id, data=saved)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        print data
        assert data['item']['saved'] == True

    def test_put_item_remove_saved(self, test_client, user_item_saved):
        self.login(test_client, user_item_saved.user.email, user_item_saved.user.password)

        saved = dict(saved=False)
        r = test_client.put('/api/items/%d' % user_item_saved.item.id, data=saved)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['saved'] == False

class TestSavedItemListAPI(TestBase):

    def test_get_items(self, test_client, user_item_saved):
        self.login(test_client, user_item_saved.user.email, user_item_saved.user.password)
        r = test_client.get('/api/items/saved')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 1

class TestTrendingItemListAPI(TestBase):

    def test_get_items_only_nonzero_votes(self, test_client, user_item_upvote, user_item):
        self.login(test_client, user_item_upvote.user.email, user_item_upvote.user.password)
        r = test_client.get('/api/items/trending')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 1


class TestFeedItemListAPI:

    def test_get_items(self, test_client, item):
        r = test_client.get('/api/feeds/%d/items' % item.feed.id)

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 1


class TestCategoryItemListAllAPI:

    def test_get_category_items_missing_category(self, test_client):
        r = test_client.get('/api/categories/nonexistent_category/items/all')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 0

    def test_get_category_items_present(self, test_client, itemsWithCategory):
        category = itemsWithCategory[0].categories[0]
        r = test_client.get('/api/categories/' + category + '/items/all')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 5


class TestCategoryItemListAPI(TestBase):

    def test_get_items_present(self, test_client, userWithPopulatedFeed):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        feed = userWithPopulatedFeed.subscribed.first()
        item = feed.items[0]
        category = item.categories[0]

        r = test_client.get('/api/categories/' + category + '/items')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 5


    def test_get_items_case_insensitive_categories(self, test_client, userWithPopulatedFeed):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        feed = userWithPopulatedFeed.subscribed.first()
        item = feed.items[0]
        category = item.categories[0].lower()

        r = test_client.get('/api/categories/' + category + '/items')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 5


    def test_get_items_category_missing(self, test_client, userWithPopulatedFeed):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        r = test_client.get('/api/categories/nonexistent_category/items')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 0


    def test_get_items_category_with_unsubscribed_item(self, test_client, userWithPopulatedFeed, itemsWithCategory):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        feed = userWithPopulatedFeed.subscribed.first()
        user_items_length = feed.items.count()
        item = feed.items[0]
        category = item.categories[0]

        r = test_client.get('/api/categories/' + category + '/items')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == user_items_length + 1
        assert len(filter(lambda item: item['feed']['subscribed'] == False, data['items'])) == 1
