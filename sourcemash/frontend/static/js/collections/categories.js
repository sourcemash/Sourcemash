Sourcemash.Collections.Categories = Backbone.Collection.extend({
	  model: Sourcemash.Models.Category,
    url: function() {
      return (this.allCategories) ? '/api/categories/all' : '/api/categories';
    },
    initialize: function(categories, options) {
      options = options || {};
      this.allCategories = options.allCategories;
    },
	  parse: function(response) {
	  	return response.categories;
	  },
	  comparator: function(item) {
	  	return [parseInt(item.get('unread_count')) === 0, item.get('title')]
	  }
});
