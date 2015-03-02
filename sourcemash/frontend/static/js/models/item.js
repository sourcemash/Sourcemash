Sourcemash.Models.Item = Backbone.Model.extend({
    urlRoot: '/api/items',

    initialize: function(data, options) {
        this.feed = options.model || new Sourcemash.Models.Feed({id: this.get('feed').id, 
										      subscribed: this.get('feed').subscribed,
    										  title: this.get('feed').title });
    }
});