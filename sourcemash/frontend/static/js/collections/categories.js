Sourcemash.Collections.Categories = Backbone.Collection.extend({
	  model: Sourcemash.Models.Category,
	  url: '/api/categories',
	  parse: function(response) {
	  	return response.categories;
	  },
	  comparator: function(item) {
	  	return [parseInt(item.get('unread_count')) === 0, item.get('category')]
	  }
});
