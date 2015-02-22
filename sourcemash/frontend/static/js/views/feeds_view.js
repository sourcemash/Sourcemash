Sourcemash.Views.FeedsView = Backbone.View.extend({
  template: JST['feeds'],
  initialize: function (options) {
    var ExtendedTypeahead = Backbone.Typeahead.extend({
      template: JST['new_feed_form'],
    });

    this.allFeeds = new Sourcemash.Collections.Feeds({url: '/api/feeds/all'})
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
    toast('Feed added!', 3000) // 3000 is the duration of the toast
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