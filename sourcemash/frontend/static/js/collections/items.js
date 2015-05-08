Sourcemash.Collections.Items = Backbone.Collection.extend({
    model: Sourcemash.Models.Item,
    url: function() {
        if (this.feed) {
            return '/api/feeds/' + this.feed.get('id') + '/items'
        } else if (this.category) {
            if (this.allItems) {
                return '/api/categories/' + this.category.get('id') + '/items/all'
            }
            return '/api/categories/' + this.category.get('id') + '/items'
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
        this.allItems = options.allItems
    },
    comparator: function(item) {
        return [-item.get('unread'), Date.parse(item.get('last_updated'))]
    }
});
