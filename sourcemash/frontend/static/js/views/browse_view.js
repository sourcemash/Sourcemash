Sourcemash.Views.BrowseView = Backbone.View.extend({
  template: JST['browse'],

  initialize: function (options) {
    var ExtendedTypeahead = Backbone.Typeahead.extend({
      template: JST['new-feed-form'],
    });

    this.typeahead = new ExtendedTypeahead({collection: this.collection, key: 'title'});
    this.listenTo(this.collection, 'sync', this.render);

    this.loading = true;
    this.user = options.user;

    this.feedCardViews = []
  },

  events: {
    'submit #add_feed_form': 'createFeed',
  },

  createFeed: function(e){
    e.preventDefault();
    if (!this.user.get('id')) {
      $("#register-modal").openModal();
      mixpanel.track("Register Modal", {"Source": "AddFeed"});
    } else {
      this.collection.create(this.newAttributes(), {success: this.updateCollection});
    };
  },

  updateCollection: function(newFeed) {
  	this.$('#url').val('');
  	newFeed.collection.fetch();
    toast('Feed added!', 3000);

    mixpanel.track("Subscribed", { "Feed Title": newFeed.get('title'),
                                    "Source": 'browse' });
  },

  render: function() {
    // Render parent view
    this.$el.html(this.template({ models: this.collection.models }));
    $('#typeahead').html(this.typeahead.render().el);

    // Render loading view
    this.loadingView = new Sourcemash.Views.LoadingView({loading: this.loading});
    this.$(".loading").html(this.loadingView.render().el);

    // Render register modal view
    this.registerModalView = new Sourcemash.Views.RegisterModalView();
    this.$("#register-modal").html(this.registerModalView.render().el);

    // Render item cards
    var feedCards = [];
    _user = this.user;
    this.collection.models.forEach(function(feed) {
        var feedCardView = new Sourcemash.Views.FeedCardView({el: "#feed-card-" + feed.get('id'),
                                                              model: feed, user: _user});
        feedCards.push(feedCardView)
    });

    this.feedCardViews = feedCards;
    return this;
  },

  _isValidURL: function(str) {
    var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
    return regexp.test(str);
  },

  newAttributes: function(){
    var url = this.$('#url').val();

    if (!this._isValidURL(url)) {
      var feed = this.collection.findWhere({'title': url});
      if (feed) {
        url = feed.get('url');
      }
    }
    return {url: url};
  },

  close: function() {
    _.each(this.feedCardViews, function(feedCardView) {
        feedCardView.close();
        feedCardView.remove();
        feedCardView.unbind();
    });

    if (this.loadingView) {
      this.loadingView.remove();
      this.loadingView.unbind();
    };

    if (this.registerModalView) {
      this.registerModalView.remove();
      this.registerModalView.unbind();
    };

  }

});
