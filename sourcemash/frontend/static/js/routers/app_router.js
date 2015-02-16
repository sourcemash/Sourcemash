Sourcemash.Routers.AppRouter = Backbone.Router.extend({
    routes: {
        "": "index",
        "feeds/:id": "show",
    },

    index: function() {
        var feedsView = new Sourcemash.Views.FeedsView({
            collection: new Sourcemash.Collections.Subscriptions()
        });

        feedsView.collection.fetch();
        this._swapView(feedsView);
    },

    show: function(id) {
        var feed = new Sourcemash.Models.Feed({ id: id });
        var feedView = new Sourcemash.Views.FeedView({ model: feed });

        feed.fetch();
        feed.items.fetch();
        this._swapView(feedView);
    },

    _swapView: function(view) {
        if (this.currentView) {
            this.currentView.remove();
        }

        this.currentView = view;
        $('#app').html(view.render().$el);
    }
})