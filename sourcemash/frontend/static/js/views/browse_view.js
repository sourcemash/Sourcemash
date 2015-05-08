Sourcemash.Views.BrowseView = Backbone.View.extend({
  template: JST['browse'],

  initialize: function (options) {
    var ExtendedTypeahead = Backbone.Typeahead.extend({
      template: JST['new-feed-form'],
    });

    this.typeahead = new ExtendedTypeahead({collection: this.collection, key: 'title'});
    this.listenTo(this.collection, 'sync', this.render);

    this.loading = true;

    this.feedTopicViews = []
  },

  events: {
    'submit #add_feed_form': 'createFeed'
  },

  createFeed: function(e){
    e.preventDefault();
    this.collection.create(this.newAttributes(), {success: this.updateCollection});
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
    this.$el.html(this.template({ models: this.feedTopicViews }));
    $('#typeahead').html(this.typeahead.render().el);

    // Render loading view
    this.loadingView = new Sourcemash.Views.LoadingView({loading: this.loading});
    this.$(".loading").html(this.loadingView.render().el);

    feeds = this.collection;
    var topicViews = [];
    Sourcemash.Views.BrowseView.FEED_TOPICS.forEach(function(topic) {
      if (feeds.length > 1) {
        var topicCards = feeds.where({topic: topic});
        var feedTopicView = new Sourcemash.Views.FeedTopicView({collection: topicCards, topic: topic,
                                                                el: "#feed-topic-" + topic});
        topicViews.push(feedTopicView);
      };
    });
    this.feedTopicViews = topicViews;

    this.$('.scrollspy').scrollSpy();
    this.$('.tabs-wrapper').pushpin({ top: this.$('.tabs-wrapper').offset().top });

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
    _.each(this.feedTopicViews, function(feedTopicView) {
        feedTopicView.close();
        feedTopicView.remove();
        feedTopicView.unbind();
    });

    if (this.loadingView) {
      this.loadingView.remove();
      this.loadingView.unbind();
    };
  }

}, {FEED_TOPICS: ['Technology', 'Business', 'Food', 'World', 'Gaming', 'Fashion', 'Photography', 'Comics', 'Science', 'Finance', 'Mash']});
