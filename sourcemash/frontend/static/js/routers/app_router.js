Sourcemash.Routers.AppRouter = Backbone.Router.extend({
    routes: {
        "": "index",
        "feeds/:id": "showFeed",
        "categories": "showCategories",
        "categories/:category": "showCategory"
    },

    index: function() {
        var feedsView = new Sourcemash.Views.FeedsView({
            collection: new Sourcemash.Collections.Feeds(),
        });

        feedsView.collection.fetch();
        feedsView.allFeeds.fetch();
        this._swapView(feedsView);
    },

    showFeed: function(id) {
        var feed = new Sourcemash.Models.Feed({ id: id });
        var feedView = new Sourcemash.Views.FeedView({ model: feed });

        feed.fetch();
        feed.items.fetch();
        this._swapView(feedView);
    },

    showCategories: function() {
        var categoriesView = new Sourcemash.Views.CategoriesView({
            collection: new Sourcemash.Collections.Categories()
        });

        categoriesView.collection.fetch();
        this._swapView(categoriesView);
    },

    showCategory: function(keyword) {
        var category = new Sourcemash.Models.Category({ category: keyword });
        var categoryView = new Sourcemash.Views.CategoryView({ model: category });

        category.fetch();
        category.items.fetch();
        this._swapView(categoryView);
    },

    _swapView: function(view) {
        if (this.currentView) {
            if (this.currentView.close) {
                this.currentView.close();
            }

            this.currentView.remove();
        }

        this.currentView = view;
        $('#app').html(view.render().$el);
    }
})