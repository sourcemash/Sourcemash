Sourcemash.Collections.Feeds = Backbone.Collection.extend({
	  model: Sourcemash.Models.Feed,
	  url: '/api/feeds',
	  parse: function(response) {
	  	return response.feeds;
	  },
	  comparator: function(feed) {
	  	return [parseInt(feed.get('unread_count')) == 0, feed.get('title')]
	  }
});