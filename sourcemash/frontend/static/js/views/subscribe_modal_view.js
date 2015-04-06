Sourcemash.Views.SubscribeModalView = Backbone.View.extend({
    template: JST['subscribe-modal'],

    initialize: function(options) {
        this.collection = options.collection;
    },

    events: {
        'click .subscribe-close': 'subscribeFromModal',
    },

    subscribeFromModal: function() {
        var item = this.collection.findWhere({title: $('#subscribe-modal #unsubscribed-item-title').text()});

        item.feed.save({'subscribed': true}, {success: this.subscribedToggled});

        mixpanel.track("Subscribed", { "Item Title": item.get('title'),
                                        "Feed Title": item.feed.get('title'),
                                        "Source": 'modal' })
    },

    subscribedToggled: function(feed) {
        if (feed.get('subscribed')) {
            toast("Subscribed!", 3000);
        } else {
            toast("You have unsubscribed...", 3000);
        }
    },

    render: function() {
        this.$el.html(this.template());
        return this;
    }
});
