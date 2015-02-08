$( document ).ready(function(){
	$(".button-collapse").sideNav();
});

$('#add_feed_form').submit(function () {
	$("#feed_url").siblings(".errors").text("")
	$("#feed_url").blur()
	append_feed()
	$("#feed_url").val("");
	return false;
})

append_feed = function() {
	$.ajax({
		type: "POST",
		url: "/api/subscriptions",
		data: {
			feed_url : $("#feed_url").val()
		},
		dataType: "json",
		error: function(data, textStatus, errorThrown) {
			errors = data.responseJSON.errors
			for (field in errors) {
				input_field = $("#"+ field)
				input_field.removeClass("valid");
				input_field.addClass("invalid");
				field_errors = input_field.siblings(".errors")
				field_errors.text(errors[field])
			}
		},
		success: function(data) {
			var subscription = data.subscription;
			subscription_view = "<p><a href='" + subscription.url + "'>" + subscription.title + "</a></p>";
			$(".feeds").append(subscription_view);
		}
	})
}

'use strict';

var feeds = {}; // create namespace for our app

//--------------
// Models
//--------------
feeds.Feed = Backbone.Model.extend({
  defaults: {
    title: '',
    url: '',
    last_updated: Date()
  }
});

//--------------
// Collections
//--------------
feeds.FeedList = Backbone.Collection.extend({
  model: feeds.Feed,
  url: '/api/subscriptions',
  parse: function(response) {
  	return response.subscriptions;
  },
  comparator: function(feed) {
  	return feed.attributes.title.toLowerCase() // alphabet sort
  }
});

// instance of the Collection
feeds.feedList = new feeds.FeedList();

//--------------
// Views
//--------------

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
  el: '#feed_list',
  initialize: function () {
    this.input = this.$('#feed_url');
    feeds.feedList.on('add', this.addAll, this);
    feeds.feedList.on('reset', this.addAll, this);
    feeds.feedList.fetch(); // Loads list from local storage
  },
  events: {
    'keypress #feed_url': 'createFeedOnEnter'
  },
  createFeedOnEnter: function(e){
    if ( e.which !== 13 || !this.input.val().trim() ) { // ENTER_KEY = 13
      return;
    }
    feeds.FeedList.create(this.newAttributes());
    this.input.val(''); // clean input box
  },
  addOne: function(feed){
    var view = new feeds.FeedView({model: feed});
    $('#feed-list').append(view.render().el);
  },
  addAll: function(){
    this.$('#feed-list').html(''); // clean the todo list
    feeds.feedList.each(this.addOne, this);
  },
  newAttributes: function(){
    return {
      url: this.input.val(),
      title: "hey there"
    }
  }
});

//--------------
// Initializers
//--------------   

feeds.FeedsView = new feeds.FeedsView(); 
