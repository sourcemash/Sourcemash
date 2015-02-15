Sourcemash.Models.Feed = Backbone.Model.extend({
    urlRoot: '/api/feeds',

    initialize: function() {
        this.items = new Sourcemash.Collections.Items([], {feed: this});
    },
    parse: function(response) {
        return response.feed;
    }
});