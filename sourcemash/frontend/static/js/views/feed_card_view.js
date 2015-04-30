Sourcemash.Views.FeedCardView = Backbone.View.extend({
    template: JST['feed-card'],

    initialize: function(options) {
        this.listenTo(this.model, 'change', this.render);
        this.render();
    },

    render: function() {
        this.$el.html(this.template({ model: this.model }));
        this.subscribeSwitchView = new Sourcemash.Views.SubscribeSwitchView({ model: this.model });
        this.$(".subscribe-switch").html(this.subscribeSwitchView.render().el);
    },

    close: function() {
        this.subscribeSwitchView.remove();
        this.subscribeSwitchView.unbind();
    }
});
