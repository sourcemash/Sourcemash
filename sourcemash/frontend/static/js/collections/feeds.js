Sourcemash.Collections.Feeds = Backbone.Collection.extend({
	  model: Sourcemash.Models.Feed,
	  url: function() {
	  	if (this.allFeeds) {
	  		return '/api/feeds/all';
	  	} else {
	  		return '/api/feeds';
	  	}
	  },
	  initialize: function(feeds, options) {
	  	feeds = feeds || [];
	  	options = options || {};
	  	this.allFeeds = options.allFeeds;
	  },
	  parse: function(response) {
	  	return response.feeds;
	  },
	  comparator: function(feed) {
	  	return [parseInt(feed.get('unread_count')) === 0, feed.get('title')]
	  }
});