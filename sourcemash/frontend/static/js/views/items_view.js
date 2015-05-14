Sourcemash.Views.ItemsView = Backbone.View.extend({
    initialize: function(options) {
        if (this.model) {
            this.listenTo(this.model, 'change:subscribed change:title', this.render);
        };
        this.listenTo(this.collection, 'change:unread', this.updateReadStatus);

        this.user = options.user;
        this.itemViews = [];
        this.loading = true;
    },

    events: {
        "click .mark-all-read": "markAllAsRead"
    },

    markAllAsRead: function() {
        var unread = this.collection.where({unread: true});
        if (unread.length > 0) {
            this.stopListening(this.collection, 'change:unread');
            this.model.save({unread: false});

            mixpanel.track("Marked all as read");
            unread.forEach(function(model) {
                model.save({unread: false});
                mixpanel.people.increment("items read");
            });
        };
    },

    updateReadStatus: function() {
        if (this.collection.length > 0 && this.collection.where({unread: true}).length == 0) {
            this.model.save({unread: false});
        };
    },

    render: function() {
        this.close();

        // Render parent view
        this.$el.html(this.template({ model: this.model, items: this.collection.models }));
        this.$('.tooltipped').tooltip({delay: 50});

        // Render subscribe modal view
        this.subscribeModalView = new Sourcemash.Views.SubscribeModalView({ collection: this.collection });
        this.$("#subscribe-modal").html(this.subscribeModalView.render().el);

        // Render loading view
        this.loadingView = new Sourcemash.Views.LoadingView({loading: this.loading});
        this.$(".loading").html(this.loadingView.render().el);

        // Render subscribe-toggle switch if feed page
        if (this.model) {
            this.subscribeSwitchView = new Sourcemash.Views.SubscribeSwitchView({ model: this.model });
            this.$(".subscribe-switch").html(this.subscribeSwitchView.render().el);
        };

        // Render item cards
        var itemCards = [];
        user = this.user;
        this.collection.models.forEach(function(item) {
            var itemCardViewTwoCol = new Sourcemash.Views.ItemCardView({el: "#item-" + item.get('id') + "-twocol", model: item, user: user });
            itemCards.push(itemCardViewTwoCol);

            var itemCardViewOneCol = new Sourcemash.Views.ItemCardView({el: "#item-" + item.get('id') + "-onecol", model: item, user: user });
            itemCards.push(itemCardViewOneCol);
        });

        this.itemViews = itemCards;
        this.updateReadStatus();
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

        if (this.loadingView) {
            this.loadingView.remove();
            this.loadingView.unbind();
        };
    }
});
