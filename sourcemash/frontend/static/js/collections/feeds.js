Sourcemash.Collections.Feeds = Backbone.Collection.extend({
	  model: Sourcemash.Models.Feed,
	  url: '/api/feeds',
	  parse: function(response) {
	  	return response.feeds;
	  },
	  comparator: 'title'
});