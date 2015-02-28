Sourcemash.Views.ItemCardView = Backbone.View.extend({
    template: JST['item-card'],
    className: "item-card",

    initialize: function(options) {
        this.feed = options.feed;
        this.items = options.items;
        this.render();
        this.listenTo(this.model, 'sync', this.render);
        this.$(".unsubscribed .upvote").one("click", _.bind(this.showSubscribeModal, this));
    },

    events: {
	  	'click .upvote': 'upvote',
	  	'click .downvote': 'downvote',
	  	'click .mark-read': 'markRead',
        'click .modal-close': 'upvote',
        'click .subscribe-close': 'subscribe'
	},

	upvote: function() {
		this.model.save({vote: 1, voteSum: this._getNewVoteSum(1)},
						{success: this.voted});
    },

	downvote: function() {
		this.model.save({vote: -1, voteSum: this._getNewVoteSum(-1)},
						{success: this.voted});
	},

	voted: function() {
		toast("Vote recorded!", 3000)
	},

    subscribe: function() {
        this.feed.save({'subscribed': true})
        this.items.fetch()
    },

    showSubscribeModal: function(e) {
        e.stopPropagation();
        this.$('.subscribe-modal').openModal();
    },

	_getNewVoteSum: function(vote) {
		return this.model.get('voteSum') + vote - this.model.get('vote')
	},

	markRead: function() {
		this.model.save({unread: false});
	},

    render: function() {
        var content = this.template({ item: this.model });
        $(content).appendTo(this.$el);
    }
});