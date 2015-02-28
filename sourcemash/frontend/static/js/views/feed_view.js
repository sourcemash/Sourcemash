Sourcemash.Views.FeedView = Sourcemash.Views.ItemsView.extend({
    template: JST['feed'],
    id: "feed-items",
    events: {
        "click #subscribe-switch": 'toggleSubscribed'
    },

    toggleSubscribed: function() {
        if (this.model.get('subscribed')) {
            this.model.save({'subscribed': false}, {success: this.toast});
            
            mixpanel.track("Unsubscribed", { "Feed Title": this.model.get('title') })
        } else {
            this.model.save({'subscribed': true}, {success: this.toast});
            
            mixpanel.track("Subscribed", { "Feed Title": this.model.get('title'),
                                            "From Modal": false })
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