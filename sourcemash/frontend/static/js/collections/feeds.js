var feeds = feeds || {}; // feeds namespace

//---------------------
// FeedList Collection
//---------------------
(function() {
	'use strict';

	feeds.FeedListCollection = Backbone.Collection.extend({
		  model: feeds.Feed,
		  url: '/api/subscriptions',
		  parse: function(response) {
		  	return response.subscriptions;
		  },
		  comparator: function(feed) { // alphabet sort
		  	return feed.attributes.title.toLowerCase() 
		  }
	});

	// instance of the Collection
	feeds.feedList = new feeds.FeedListCollection();
	
})();