Sourcemash.Views.ItemsView = Backbone.View.extend({
    initialize: function(options) {
        if (this.model) {
            this.listenTo(this.model, 'change', this.render);
        }

        this.itemViews = [];
    },

    events: {
        "click #subscribe-switch": 'subscribeFromSwitch',
        'click .subscribe-close': 'subscribeFromModal',
    },

    subscribeFromSwitch: function() {
        if (this.model.get('subscribed')) {
            this.model.save({'subscribed': false}, {success: this.subscribed});
            
            mixpanel.track("Unsubscribed", { "Feed Title": this.model.get('title') })
        } else {
            this.model.save({'subscribed': true}, {success: this.subscribed});
            
            mixpanel.track("Subscribed", { "Feed Title": this.model.get('title'),
                                            "Source": 'feed page' })
        }
    },

    subscribeFromModal: function() {
        var item = this.collection.findWhere({title: $('#subscribe-modal #unsubscribed-item-title').text()});

        item.feed.save({'subscribed': true}, {success: this.subscribed})

        mixpanel.track("Subscribed", { "Item Title": item.get('title'),
                                        "Feed Title": item.feed.get('title'),
                                        "Source": 'modal' })
    },

    subscribed: function(feed) {
        if (feed.get('subscribed')) {
            toast("Subscribed!", 3000);
        } else {
            toast("You have unsubscribed...", 3000);
        }
    },

    render: function() {
        // Render parent view
        this.$el.html(this.template({ model: this.model, items: this.collection.models }));

        // Render item cards
        this.close();
        var itemCards = [];
        this.collection.models.forEach(_.bind(function(item) {
            var itemCardView = new Sourcemash.Views.ItemCardView({el: "#item-" + item.get('id'), model: item});
            itemCards.push(itemCardView)
        }, this))

        this.itemViews = itemCards;
        return this;
    },

    close: function() {
        _.each(this.itemViews, function(itemView) {
            itemView.remove();
            itemView.unbind();
        })
    }
});
