Sourcemash.Collections.Items = Backbone.Collection.extend({
    model: Sourcemash.Models.Item,
    url: function() {
        if (this.feed) {
            return '/api/feeds/' + this.feed.get('id') + '/items'
        } else if (this.category) {
            return '/api/categories/' + this.category.get('category') + '/items'
        }
    },
    parse: function(response) {
        return response.items;
    },
    initialize: function(items, options) {
        this.feed = options.feed;
        this.category = options.category;
    },
    comparator: function(item) {
        return [-item.get('unread'), -Date.parse(item.get('last_updated'))]
    }
});