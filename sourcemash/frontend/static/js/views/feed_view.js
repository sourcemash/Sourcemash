Sourcemash.Views.FeedView = Sourcemash.Views.ItemsView.extend({
    template: JST['feed'],
    id: "feed-items",
    events: {
        "click #subscribe-switch": 'toggleSubscribed'
    },

    toggleSubscribed: function() {
        if (this.model.get('subscribed')) {
            this.model.save({'subscribed': false}, {success: this.toast});
        } else {
            this.model.save({'subscribed': true}, {success: this.toast});
        }
        this.model.items.fetch();
    },

    toast: function(feed) {
        if (feed.get('subscribed')) {
            toast("Subscribed!", 3000);
        } else {
            toast("You have unsubscribed...", 3000);
        }
    }
});