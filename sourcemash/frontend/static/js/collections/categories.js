Sourcemash.Collections.Categories = Backbone.Collection.extend({
	  model: Sourcemash.Models.Category,
    url: '/api/categories',
	  parse: function(response) {
	  	return response.categories;
	  },
	  comparator: function(category) {
	  	return [!category.get('unread'), category.get('name')]
	  }
});
