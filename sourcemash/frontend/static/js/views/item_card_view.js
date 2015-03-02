Sourcemash.Views.ItemCardView = Backbone.View.extend({
    template: JST['item-card'],

    initialize: function(options) {
        this.listenTo(this.model, 'change', this.render);
        this.render();
    },

    events: {
	  	'click .upvote': 'upvote',
	  	'click .downvote': 'downvote',
	  	'click .mark-read': 'markRead',
        'click .saved': 'saveToggled'
	},

	upvote: function() {
		this.model.save({vote: 1, voteSum: this._getNewVoteSum(1)},
                        {success: this.voted});
        
        if (this.model.changedAttributes()) {
            mixpanel.track("Upvoted", { "Item Title": this.model.get('title'),
                                        "Feed Title": this.model.feed.get('title') })

            if (!this.model.feed.get('subscribed')) {
                this.showSubscribeModal();
            }
        }
    },

	downvote: function() {
		this.model.save({vote: -1, voteSum: this._getNewVoteSum(-1)},
                        {success: this.voted});
        
        if (this.model.changedAttributes()) {
            mixpanel.track("Downvoted", { "Item Title": this.model.get('title'),
                                        "Feed Title": this.model.feed.get('title') })
        }
	},

    voted: function() {
        toast("Vote recorded!", 3000);
    },

    showSubscribeModal: function(e) {
        $('#subscribe-modal #unsubscribed-item-title').html(this.model.get('title'));
        $('#subscribe-modal #unsubscribed-feed-title').html(this.model.feed.get('title'));
        $('#subscribe-modal').openModal();
        
        mixpanel.track("Subscribe Modal", { "Item Title": this.model.get('title'),
                                            "Feed Title": this.model.feed.get('title') })
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

    saveToggled: function() {
        if (this.model.get('saved')) {
            this.model.save({saved: false},
                {success: this.savedToast});
            
            if (this.model.changedAttributes()) {
            mixpanel.track("Saved", { "Item Title": this.model.get('title'),
                                        "Feed Title": this.model.feed.get('title') });
            }

        } else {
            this.model.save({saved: true},
                {success: this.savedToast});            
        }

    },

    savedToast: function(item) {
        if (item.get('saved')) {
            toast("Saved!", 3000);
        } else {
            toast("Unsaved...", 3000)
        }
    },

    openCard: function() {
      this.$('.card-reveal').velocity({translateY: '-100%'}, {duration: 300, queue: false, easing: 'easeInOutQuad'});
    },

    render: function() {
        this.$el.html(this.template({ item: this.model }));
    }
});