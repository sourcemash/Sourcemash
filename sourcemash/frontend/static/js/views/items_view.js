Sourcemash.Views.ItemsView = Backbone.View.extend({
    initialize: function(options) {
        if (this.model) {
            this.listenTo(this.model, 'change:subscribed', this.render);
        };

        this.itemViews = [];
    },

    events: {
        "click .mark-all-read": "markAllAsRead"
    },

    markAllAsRead: function() {
        var unread = this.collection.where({unread: true});
        unread.forEach(function(model) {
            model.save({unread: false});
        });
        this.model.set({unread_count: 0});
    },

    render: function() {
        this.close();

        // Render parent view
        this.$el.html(this.template({ model: this.model, items: this.collection.models }));

        // Render subscribe modal view
        this.subscribeModalView = new Sourcemash.Views.SubscribeModalView({ collection: this.collection });
        this.$("#subscribe-modal").html(this.subscribeModalView.render().el);

        // Render subscribe-toggle switch if feed page
        if (this.model) {
            this.subscribeSwitchView = new Sourcemash.Views.SubscribeSwitchView({ model: this.model });
            this.$(".subscribe-switch").html(this.subscribeSwitchView.render().el);
        };

        // Render item cards
        var itemCards = [];
        this.collection.models.forEach(function(item) {
            var itemCardView = new Sourcemash.Views.ItemCardView({el: "#item-" + item.get('id'), model: item});
            itemCards.push(itemCardView)
        });

        this.itemViews = itemCards;
        return this;
    },

    close: function() {
        _.each(this.itemViews, function(itemView) {
            itemView.remove();
            itemView.unbind();
        });

        if (this.subscribeModalView) {
            this.subscribeModalView.remove();
            this.subscribeModalView.unbind();
        };

        if (this.subscribeSwitchView) {
            this.subscribeSwitchView.remove();
            this.subscribeSwitchView.unbind();
        };
    }
});
