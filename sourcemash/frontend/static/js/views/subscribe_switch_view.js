Sourcemash.Views.SubscribeSwitchView = Backbone.View.extend({
    template: JST['subscribe-switch'],

    initialize: function() {
        this.listenTo(this.model, 'change', this.render);
    },

    events: {
        "click .subscribe-toggle": 'subscribeFromSwitch',
	},

    subscribeFromSwitch: function() {
        if (this.model.get('subscribed')) {
            this.model.save({'subscribed': false}, {success: this.subscribedToggled});
            
            mixpanel.track("Unsubscribed", { "Feed Title": this.model.get('title') })
        } else {
            this.model.save({'subscribed': true}, {success: this.subscribedToggled});
            
            mixpanel.track("Subscribed", { "Feed Title": this.model.get('title'),
                                            "Source": 'feed card' })
        }
    },

    subscribedToggled: function(feed) {
      if (feed.get('subscribed')) {
          toast("Subscribed!", 3000);
      } else {
          toast("You have unsubscribed...", 3000);
      }
    },

    render: function() {
        this.$el.html(this.template({ model: this.model }));
        return this;
    }
});