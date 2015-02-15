Sourcemash.Views.FeedView = Backbone.View.extend({
    template: JST['feed'],

    initialize: function(options) {
        this.listenTo(this.model, 'sync', this.render);
        this.listenTo(this.model.items, 'sync', this.render);
    },

    render: function() {
        var content = this.template({ feed: this.model });
        this.$el.html(content);
        return this;
    },

    refresh: function(event) {
        this.model.entries.fetch();
    }
});