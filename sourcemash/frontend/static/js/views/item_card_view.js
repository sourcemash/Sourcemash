Sourcemash.Views.ItemCardView = Backbone.View.extend({
    template: JST['item-card'],

    initialize: function(options) {
        this.feed = options.feed;
        this.listenTo(this.model, 'change', this.render);

        this.render();
    },

    events: {
	  	'click .upvote': 'upvote',
	  	'click .downvote': 'downvote',
	  	'click .mark-read': 'markRead',
	},

	upvote: function() {
		this.model.save({vote: 1, voteSum: this._getNewVoteSum(1)},
                        {success: this.voted});
        
        if (this.model.changedAttributes()) {
            mixpanel.track("Upvoted", { "Item Title": this.model.get('title'),
                                        "Feed Title": this.feed.get('title') })

            if (!this.feed.get('subscribed')) {
                this.showSubscribeModal();
            }
        }
    },

	downvote: function() {
		this.model.save({vote: -1, voteSum: this._getNewVoteSum(-1)},
                        {success: this.voted});
        
        if (this.model.changedAttributes()) {
            mixpanel.track("Downvoted", { "Item Title": this.model.get('title'),
                                        "Feed Title": this.feed.get('title') })
        }
	},

    voted: function() {
        toast("Vote recorded!", 3000);
    },

    showSubscribeModal: function(e) {
        $('#subscribe-modal #unsubscribed-item-title').html(this.model.get('title'));
        $('#subscribe-modal #unsubscribed-feed-title').html(this.feed.get('title'));
        $('#subscribe-modal').openModal();
        
        mixpanel.track("Subscribe Modal", { "Item Title": this.model.get('title'),
                                            "Feed Title": this.feed.get('title') })
    },

	_getNewVoteSum: function(vote) {
		return this.model.get('voteSum') + vote - this.model.get('vote')
	},

	markRead: function() {
		this.model.save({unread: false},
                        {success: _.bind(this.openCard, this)});
        
        if (this.model.changedAttributes()) {
            mixpanel.people.increment("items read")
        }
	},

    openCard: function() {
      this.$('.card-reveal').velocity({translateY: '-100%'}, {duration: 300, queue: false, easing: 'easeInOutQuad'});
    },

    render: function() {
        this.$el.html(this.template({ item: this.model }));
    }
});