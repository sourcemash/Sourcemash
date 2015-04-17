Sourcemash.Models.Feed = Backbone.Model.extend({
    urlRoot: '/api/feeds',

    parse: function (response) {
        if (response.feed) {
            return response.feed;
        };
        return response;
    }
});
