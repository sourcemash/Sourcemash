Sourcemash.Views.ItemView = Backbone.View.extend({
    template: JST['item'],

    initialize: function(options) {
    	this.parent = options.parent;
        this.render();
        this.listenTo(this.model, 'sync', this.render);
    },

    events: {
	  	'click .upvote': 'upvote',
	  	'click .downvote': 'downvote'
	},

	upvote: function() {
		this.model.save({'vote': 1}, {success: this.voted});
	},

	downvote: function() {
		this.model.save({'vote': -1}, {success: this.voted});
	},

	voted: function(item) {
		item.collection.fetch()	// Force ItemsView refresh
		toast("Vote recorded!", 3000)
	},

    render: function() {
        var content = this.template({ item: this.model });
        $(content).appendTo(this.$el);
    }
});