Sourcemash.Collections.CategoryItems = Backbone.Collection.extend({
    model: Sourcemash.Models.Item,
    url: function() {
        return '/api/categories/' + this.category.get('category')
    },
    parse: function(response) {
        return response.items;
    },
    initialize: function(items, options) {
        this.category = options.category;
    }
});