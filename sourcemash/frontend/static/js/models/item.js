Sourcemash.Models.Item = Backbone.Model.extend({
    urlRoot: '/api/items',

    initialize: function(data, options) {
        var existingFeed = options.feeds.findWhere({id: this.get('feed').id});

        if (existingFeed) {
            this.feed = existingFeed;
        } else {
            this.feed = new Sourcemash.Models.Feed({id: this.get('feed').id,
                                          subscribed: this.get('feed').subscribed,
                                          title: this.get('feed').title });
            options.feeds.add(this.feed);
        };

        this.categories = new Sourcemash.Collections.Categories();
        _.each(this.get('categories'), function(category) {
            var existingCategory = options.categories.findWhere({id: category.id});

            if (existingCategory) {
                this.categories.add(existingCategory);
            } else {
                var newCategory = new Sourcemash.Models.Category({id: category.id, name: category.name});
                this.categories.add(newCategory);
            };
        }, this);
    }
});
