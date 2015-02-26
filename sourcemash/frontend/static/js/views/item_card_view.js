Sourcemash.Views.ItemCardView = Backbone.View.extend({
    template: JST['item-card'],
    className: "item-card",

    initialize: function(options) {
        this.render();
        this.listenTo(this.model, 'sync', this.render);
    },

    events: {
	  	'click .upvote': 'upvote',
	  	'click .downvote': 'downvote',
	  	'mouseover #mark-read': 'markRead',
	  	'click #mark-unread': 'markUnread'
	},

	upvote: function() {
		this.model.save({'vote': 1, 'voteSum': this._getNewVoteSum(1)},
						{success: this.voted});
	},

	downvote: function() {
		this.model.save({'vote': -1, 'voteSum': this._getNewVoteSum(-1)},
						{success: this.voted});
	},

	voted: function() {
		toast("Vote recorded!", 3000)
	},

	_getNewVoteSum: function(vote) {
		return this.model.get('voteSum') + vote - this.model.get('vote')
	},

	markRead: function() {
		this.model.save({'mark_read': true, 'unread': false});
	},

	markUnread: function() {
		this.model.save({'mark_unread': true, 'unread': true});
	},

    render: function() {
        var content = this.template({ item: this.model });
        $(content).appendTo(this.$el);
    }
});