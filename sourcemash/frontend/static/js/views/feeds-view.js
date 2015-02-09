var feeds = feeds || {}; // feeds namespace

//---------------------
// Feed, FeedList Views
//---------------------
(function($) {
	'use strict';

	// renders individual todo items list (li)
	feeds.FeedView = Backbone.View.extend({
	  tagName: 'li',
	  template: _.template($('#feed-template').html()),
	  render: function(){
	    this.$el.html(this.template(this.model.toJSON()));
	    return this; // enable chained calls
	  }
	});

	// renders the full list of todo items calling TodoView for each one.
	feeds.FeedsView = Backbone.View.extend({
	  el: '.feeds',
	  initialize: function () {
	    this.input = $('#url');
	    this.csrf = $("#csrf_token")
	    feeds.feedList.on('sync', this.addAll, this);
	    feeds.feedList.fetch(); 
	  },
	  events: {
	    'keypress #url': 'createFeedOnEnter',
	    'click button[type="submit"]': 'createFeedOnClick'
	  },
	  createFeedOnClick: function(e){
	    feeds.feedList.create(this.newAttributes(), {wait: true, success: this.clear_input});
	    feeds.feedList.fetch(); // forced refresh
	    return false;
	  },
	  createFeedOnEnter: function(e){
	  	if ( e.which !== 13 || !this.input.val().trim() ) { // ENTER_KEY = 13
	      return;
	    }
	    feeds.feedList.create(this.newAttributes(), {wait: true, success: this.clear_input});
	    feeds.feedList.fetch(); // forced refresh
	    return false;
	  },
	  clear_input: function() {
	  	$('#url').val('');
	  },
	  addOne: function(feed){
	    var view = new feeds.FeedView({model: feed});
	    $('#feed-list').append(view.render().el);
	  },
	  addAll: function(){
	    $('#feed-list').html(''); // clean the todo list
	    feeds.feedList.each(this.addOne, this);
	  },
	  newAttributes: function(){
	    return {
	      url: this.input.val(),
	      csrf_token: this.csrf.val()
	    }
	  }
	});

//--------------
// Initializers
//--------------   

feeds.FeedsView = new feeds.FeedsView(); 
	
})(jQuery);