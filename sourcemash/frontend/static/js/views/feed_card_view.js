Sourcemash.Views.FeedCardView = Backbone.View.extend({
    template: JST['feed-card'],

    initialize: function(options) {
        this.listenTo(this.model, 'change', this.render);
        this.render();
    },

    events: {
        "click #subscribe-switch": 'toggleSubscribe',
	},

    toggleSubscribe: function() {
        if (this.model.get('subscribed')) {
            this.model.save({'subscribed': false}, {success: this.subscribed});
            
            mixpanel.track("Unsubscribed", { "Feed Title": this.model.get('title') })
        } else {
            this.model.save({'subscribed': true}, {success: this.subscribed});
            
            mixpanel.track("Subscribed", { "Feed Title": this.model.get('title'),
                                            "Source": 'feed page' })
        }
        },

        subscribed: function(feed) {
          if (feed.get('subscribed')) {
              toast("Subscribed!", 3000);
          } else {
              toast("You have unsubscribed...", 3000);
          }
    },

    render: function() {
        this.$el.html(this.template({ model: this.model }));
    }
});