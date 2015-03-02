Sourcemash.Routers.AppRouter = Backbone.Router.extend({
    routes: {
        "": "showProfile",
        "feeds": "showFeeds",
        "feeds/:id": "showFeed",
        "categories": "showCategories",
        "categories/:category": "showCategory",
        "saved": "showSaved",
        "browse/feeds": "browseFeeds"
    },

    showProfile: function() {
        var user = new Sourcemash.Models.User()
        var profileView = new Sourcemash.Views.ProfileView({ model: user });

        user.fetch({success: this._identifyUser});
        this._swapView(profileView);
    },

    showFeeds: function() {
        var feedsView = new Sourcemash.Views.FeedsView({
            collection: new Sourcemash.Collections.Feeds(),
        });

        feedsView.collection.fetch();
        feedsView.allFeeds.fetch({url: '/api/feeds/all'});
        this._swapView(feedsView);
    },

    browseFeeds: function() {
        var browseView = new Sourcemash.Views.BrowseView({
            collection: new Sourcemash.Collections.Feeds(),
        });

        browseView.collection.fetch({url: '/api/feeds/all'});
        this._swapView(browseView);
    },

    showFeed: function(id) {
        var feed = new Sourcemash.Models.Feed({ id: id });
        var feeds = new Sourcemash.Collections.Feeds([feed]);
        var feedItems = new Sourcemash.Collections.Items([], {feed: feed});
        var feedView = new Sourcemash.Views.FeedView({ model: feed, collection: feedItems });

        feed.fetch();
        feedView.collection.fetch({feeds: feeds, success: function() {feedView.render()}});
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
        var feeds = new Sourcemash.Collections.Feeds();
        var category = new Sourcemash.Models.Category({ category: keyword });
        var categoryItems = new Sourcemash.Collections.Items([], {category: category});
        var categoryView = new Sourcemash.Views.CategoryView({ model: category, collection: categoryItems });

        categoryView.collection.fetch({feeds: feeds, success: function() {categoryView.render()}});
        this._swapView(categoryView);
    },

    showSaved: function() {
        var feeds = new Sourcemash.Collections.Feeds();
        var savedItems = new Sourcemash.Collections.Items([], {saved: true});
        var savedView = new Sourcemash.Views.SavedView({ collection: savedItems });

        savedView.collection.fetch({feeds: feeds, success: function() {savedView.render()}});
        this._swapView(savedView);
    },

    _swapView: function(view) {
        if (this.currentView) {
            if (this.currentView.close) {
                this.currentView.close();
            }

            this.currentView.remove();
            this.currentView.unbind();
        }

        this.currentView = view;
        $('#app').html(view.render().$el);
    },

    _identifyUser: function(user) {
        mixpanel.identify(user.get('email'));
        mixpanel.people.set_once('$created', new Date());
        mixpanel.people.set({
            "$email": user.get('email')
        });
    }
})