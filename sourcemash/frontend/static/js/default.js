$( document ).ready(function(){
	$(".button-collapse").sideNav();
});

// 'use strict';

// var feeds = {}; // create namespace for our app

// //--------------
// // Models
// //--------------
// feeds.Feed = Backbone.Model.extend({
//   defaults: {
//     url: '',
//     title: ''
//   }
// });

// //--------------
// // Collections
// //--------------
// feeds.FeedListCollection = Backbone.Collection.extend({
//   model: feeds.Feed,
//   url: '/api/subscriptions',
//   parse: function(response) {
//   	return response.subscriptions;
//   },
//   comparator: function(feed) {
//   	return feed.attributes.title.toLowerCase() // alphabet sort
//   }
// });

// // instance of the Collection
// feeds.feedList = new feeds.FeedListCollection();

// //--------------
// // Views
// //--------------

// // renders individual todo items list (li)
// feeds.FeedView = Backbone.View.extend({
//   tagName: 'li',
//   template: _.template($('#feed-template').html()),
//   render: function(){
//     this.$el.html(this.template(this.model.toJSON()));
//     return this; // enable chained calls
//   }
// });

// // renders the full list of todo items calling TodoView for each one.
// feeds.FeedsView = Backbone.View.extend({
//   el: '.feeds',
//   initialize: function () {
//     this.input = $('#feed_url');
//     feeds.feedList.on('sync', this.addAll, this);
//     feeds.feedList.fetch(); 
//   },
//   events: {
//     'keypress #feed_url': 'keyPressEventHandler',
//     'click button[type="submit"]': 'createFeedOnEnter'
//   },
//   createFeedOnEnter: function(e){
//     e.stopPropagation();
//     feeds.feedList.create(this.newAttributes(), {wait: true});
//     this.input.val(''); // clean input box
//     feeds.feedList.fetch(); // forced refresh
//     return false;
//   },
//   keyPressEventHandler: function(e){
//   	if ( e.which !== 13 || !this.input.val().trim() ) { // ENTER_KEY = 13
//       return;
//     }
//     feeds.feedList.create(this.newAttributes(), {wait: true});
//     this.input.val(''); // clean input box
//     feeds.feedList.fetch(); // forced refresh
//     return false;
//   },
//   addOne: function(feed){
//     var view = new feeds.FeedView({model: feed});
//     $('#feed-list').append(view.render().el);
//   },
//   addAll: function(){
//     $('#feed-list').html(''); // clean the todo list
//     feeds.feedList.each(this.addOne, this);
//   },
//   newAttributes: function(){
//     return {
//       feed_url: this.input.val()
//     }
//   }
// });

// Backbone.View.prototype.close = function() {
// 	this.remove();
// 	this.unbind();
// };

// //--------------
// // Initializers
// //--------------   

// feeds.FeedsView = new feeds.FeedsView(); 
