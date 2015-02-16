Sourcemash.Collections.Items = Backbone.Collection.extend({
    model: Sourcemash.Models.Item,
    url: function() {
        return '/api/feeds/' + this.feed.get('id') + '/items'
    },
    parse: function(response) {
        return response.items;
    },
    initialize: function(items, options) {
        this.feed = options.feed;
    }
});