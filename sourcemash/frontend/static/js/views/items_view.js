Sourcemash.Views.ItemsView = Backbone.View.extend({
    initialize: function(options) {
        if (this.model) {
            this.listenTo(this.model, 'change', this.render);
        }

        this.itemViews = [];
    },

    events: {
        'click .subscribe-close': 'subscribeFromModal',
    },

    subscribeFromModal: function() {
        var item = this.collection.findWhere({title: $('#subscribe-modal #unsubscribed-item-title').text()});

        item.feed.save({'subscribed': true}, {success: this.subscribedToggled})

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
        this.close();
        
        // Render parent view
        this.$el.html(this.template({ model: this.model, items: this.collection.models }));

        // Render subscribe-toggle switch if feed page
        if (this.model) {
            this.subscribeSwitchView = new Sourcemash.Views.SubscribeSwitchView({ model: this.model });
            this.$(".subscribe-switch").html(this.subscribeSwitchView.render().el)
        }

        // Render item cards
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
        });

        if (this.subscribeSwitchView) {
            this.subscribeSwitchView.remove();
            this.subscribeSwitchView.unbind();
        };
    }
});
