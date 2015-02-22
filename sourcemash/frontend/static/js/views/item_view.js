Sourcemash.Views.ItemView = Backbone.View.extend({
    template: JST['item'],
    className: "col m6",

    initialize: function(options) {
        this.render();
        this.listenTo(this.model, 'sync', this.render);
    },

    events: {
	  	'click .upvote': 'upvote',
	  	'click .downvote': 'downvote'
	},

	upvote: function(e) {
		e.stopPropagation()
		this.model.save({'vote': 1, 'voteSum': this._getNewVoteSum(1)},
						{success: this.voted});
	},

	downvote: function(e) {
		e.stopPropagation()
		this.model.save({'vote': -1, 'voteSum': this._getNewVoteSum(-1)},
						{success: this.voted});
	},

	voted: function() {
		toast("Vote recorded!", 3000)
	},

	_getNewVoteSum: function(vote) {
		return this.model.get('voteSum') + vote - this.model.get('vote')
	},

    render: function() {
        var content = this.template({ item: this.model });
        $(content).appendTo(this.$el);
    }
});