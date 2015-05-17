Sourcemash.Routers.AppRouter = Backbone.Router.extend({
    routes: {
        "": "showSplash",
        "profile": "showProfile",
        "feeds/:id": "showFeed",
        "categories/:id": "showCategory",
        "saved": "showSaved",
        "browse": "browseFeeds"
    },

    initialize: function(options){
        var self = this;

        self._user = new Sourcemash.Models.User();
        self._feeds = new Sourcemash.Collections.Feeds([], {allFeeds: true});
        self._categories = new Sourcemash.Collections.Categories();

        self._sidenav = new Sourcemash.Views.SidenavView({ user: self._user, feeds: self._feeds, categories: self._categories });
        $('#nav-mobile').html(self._sidenav.render().$el);

        self._registerModalView = new Sourcemash.Views.RegisterModalView();
        $("#register-modal").html(self._registerModalView.render().$el);

        self._forgotModalView = new Sourcemash.Views.ForgotModalView();
        $("#forgot-modal").html(self._forgotModalView.render().$el);

        self._user.fetch({success: this._identifyUser});
        self._sidenav.feeds.reset(self._feeds);
        self._sidenav.categories.reset(self._categories);

        self._sidenav.render();
        self._feeds.fetch();
        self._categories.fetch({success: _.bind(function() {this._loaded(this._sidenav)}, this)});
    },

    showSplash: function() {
        var splashView = new Sourcemash.Views.SplashView();
        this._swapView(splashView);
        mixpanel.track("Visited Landing Page");
    },

    showProfile: function() {
        var profileView = new Sourcemash.Views.ProfileView({ model: this._user });
        this._swapView(profileView);
        mixpanel.track("Visited Profile Page");
    },

    browseFeeds: function() {
        var browseView = new Sourcemash.Views.BrowseView({ collection: this._feeds });
        browseView.collection.fetch({success: _.bind(function() {this._loaded(browseView)}, this)});
        this._swapView(browseView);
        mixpanel.track("Visited Browse Page");
    },

    showFeed: function(id) {
        var feed = new Sourcemash.Models.Feed({ id: id });
        feed = this._feeds.add(feed);

        var feedItems = new Sourcemash.Collections.Items([], {feed: feed});
        var feedView = new Sourcemash.Views.FeedView({ model: feed, collection: feedItems, user: this._user });

        feed.fetch();
        feedView.collection.fetch({feeds: this._feeds, categories: this._categories, success: _.bind(function() {this._loaded(feedView)}, this)});
        this._swapView(feedView);
        mixpanel.track("Visited Feed Page", {"Feed Title": feed.get('title')});
    },

    showCategory: function(id) {
        var category = new Sourcemash.Models.Category({ id: id });
        var categoryItems = new Sourcemash.Collections.Items([], {category: category, allItems: this._user.get('email') ? false : true});
        var categoryView = new Sourcemash.Views.CategoryView({ model: category, collection: categoryItems, user: this._user });

        category.fetch();
        categoryView.collection.fetch({feeds: this._feeds, categories: this._categories, success: _.bind(function() {this._loaded(categoryView)}, this)});
        this._swapView(categoryView);
        mixpanel.track("Visited Category Page", {"Category Title": category.get('name')});

    },

    showSaved: function() {
        var savedItems = new Sourcemash.Collections.Items([], {saved: true});
        var savedView = new Sourcemash.Views.SavedView({ collection: savedItems, user: this._user });

        savedView.collection.fetch({feeds: this._feeds, categories: this._categories, success: _.bind(function() {this._loaded(savedView)}, this)});
        this._swapView(savedView);
        mixpanel.track("Visited Saved Page");
    },

    _loaded: function(view) {
        view.loading = false;
        view.render();
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
