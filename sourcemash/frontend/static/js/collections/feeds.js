Sourcemash.Collections.Feeds = Backbone.Collection.extend({
	  model: Sourcemash.Models.Feed,
	  url: function() {
	  	return (this.allFeeds) ? '/api/feeds/all' : '/api/feeds';
	  },
	  initialize: function(feeds, options) {
	  	options = options || {};
	  	this.allFeeds = options.allFeeds;
	  },
	  parse: function(response) {
	  	return response.feeds;
	  },
	  comparator: function(feed) {
	  	return [!feed.get('unread'), feed.get('title')]
	  }
});
