Sourcemash.Views.FeedsView = Backbone.View.extend({
  template: JST['feeds'],
  initialize: function () {
    this.listenTo(this.collection, 'add sync remove change', this.render);
  },
  events: {
    'submit #add_feed_form': 'createFeed'
  },
  createFeed: function(e){
  	e.preventDefault()
    this.collection.create(this.newAttributes(), {wait: true, url: this.collection.url, success: this.updateCollection});
  },
  updateCollection: function(newFeed) {
  	this.$('#url').val('');
  	newFeed.collection.fetch();
  },
  render: function() {
  	var content = this.template({feeds: this.collection.models})
  	this.$el.html(content);
  	return this;
  },
  newAttributes: function(){
    return {
      url: this.$('#url').val().trim(),
    }
  }
});