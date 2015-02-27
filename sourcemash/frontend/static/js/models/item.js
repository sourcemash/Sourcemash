Sourcemash.Models.Item = Backbone.Model.extend({
    urlRoot: '/api/items',

    initialize: function() {
        this.feed = new Sourcemash.Models.Feed({id: this.get('feed').id});
    }
});