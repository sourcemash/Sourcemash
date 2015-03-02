Sourcemash.Collections.Items = Backbone.Collection.extend({
    model: Sourcemash.Models.Item,
    url: function() {
        if (this.feed) {
            return '/api/feeds/' + this.feed.get('id') + '/items'
        } else if (this.category) {
            return '/api/categories/' + this.category.get('category') + '/items'
        } else if (this.saved) {
            return '/api/items/saved'
        }
    },
    parse: function(response) {
        return response.items;
    },
    initialize: function(items, options) {
        this.feed = options.feed;
        this.category = options.category;
        this.saved = options.saved;
    },
    comparator: function(item) {
        return [-item.get('unread'), Date.parse(item.get('last_updated'))]
    }
});