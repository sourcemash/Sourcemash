Sourcemash.Routers.AppRouter = Backbone.Router.extend({
    routes: {
        "": "showSplash",
        "profile": "showProfile",
        "feeds/:id": "showFeed",
        "categories/:category": "showCategory",
        "saved": "showSaved",
        "browse": "browseFeeds"
    },

    initialize: function(options){
        var self = this;

        self._user = new Sourcemash.Models.User();
        self._feeds = new Sourcemash.Collections.Feeds();
        self._categories = new Sourcemash.Collections.Categories();

        self._sidenav = new Sourcemash.Views.SidenavView({ user: self._user, feeds: self._feeds, categories: self._categories });

        self._user.fetch({success: this._identifyUser});
        self._sidenav.feeds.fetch();
        self._sidenav.categories.fetch();

        $('#nav-mobile').html(self._sidenav.render().$el);
    },

    showSplash: function() {
        var splashView = new Sourcemash.Views.SplashView();
        this._swapView(splashView);
    },

    showProfile: function() {
        var profileView = new Sourcemash.Views.ProfileView({ model: this._user });
        this._swapView(profileView);
    },

    browseFeeds: function() {
        var browseView = new Sourcemash.Views.BrowseView({
            collection: new Sourcemash.Collections.Feeds([], {allFeeds: true}),
        });

        browseView.collection.fetch();
        this._swapView(browseView);
    },

    showFeed: function(id) {
        var feed = new Sourcemash.Models.Feed({ id: id });
        var feeds = new Sourcemash.Collections.Feeds([feed], {});
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
        $('#main').html(view.render().$el);
    },

    _identifyUser: function(user) {
        mixpanel.identify(user.get('email'));
        mixpanel.people.set_once('$created', new Date());
        mixpanel.people.set({
            "$email": user.get('email')
        });
    }
})
