Sourcemash.Views.SubscribeSwitchView = Backbone.View.extend({
    template: JST['subscribe-switch'],

    initialize: function(options) {
        this.user = options.user;
        this.listenTo(this.model, 'change', this.render);
    },

    events: {
        "click .subscribe-toggle": 'subscribeFromSwitch',
	},

    subscribeFromSwitch: function() {
        if (this.model.get('subscribed')) {
            this.model.save({'subscribed': false}, {success: this.subscribedToggled});

        } else {
            this.model.save({'subscribed': true}, {success: this.subscribedToggled});


        };
    },

    subscribedToggled: function(feed) {
      if (feed.get('subscribed')) {
        toast("Subscribed!", 3000);
        mixpanel.track("Subscribed", { "Feed Title": feed.get('title'),
                                            "Source": 'feed card' })
      } else {
        toast("You have unsubscribed...", 3000);
        mixpanel.track("Unsubscribed", { "Feed Title": feed.get('title') })
      }
    },

    render: function() {
        this.$el.html(this.template({ model: this.model }));
        return this;
    }
});
