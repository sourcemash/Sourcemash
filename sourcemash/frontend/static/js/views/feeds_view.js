Sourcemash.Views.FeedsView = Backbone.View.extend({
  template: JST['feeds'],
  initialize: function (options) {
    var ExtendedTypeahead = Backbone.Typeahead.extend({
      template: JST['new-feed-form'],
    });

    this.allFeeds = new Sourcemash.Collections.Feeds([], {allFeeds: true})
    this.typeahead = new ExtendedTypeahead({collection: this.allFeeds, key: 'title'});
    this.listenTo(this.collection, 'sync', this.render);
  },
  events: {
    'submit #add_feed_form': 'createFeed'
  },
  createFeed: function(e){
  	e.preventDefault()
    this.collection.create(this.newAttributes(), {success: this.updateCollection});
  },
  updateCollection: function(newFeed) {
  	this.$('#url').val('');
  	newFeed.collection.fetch();
    toast('Feed added!', 3000)

    mixpanel.track("Subscribed", { "Feed Title": newFeed.get('title'),
                                    "Source": 'search' })
  },
  render: function() {
  	var content = this.template({feeds: this.collection.models})
  	this.$el.html(content);
    $('#typeahead').html(this.typeahead.render().el);
  	return this;
  },
  newAttributes: function(){
    var url = this.$('#url').val()
    
    if (!this._isValidURL(url)) {
      var feed = this.allFeeds.findWhere({'title': url});
      if (feed) {
        url = feed.get('url');
      }
    }

    return {
      url: url,
    }
  },
  _isValidURL: function(str) {
    var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/
    return regexp.test(str);
  }
});