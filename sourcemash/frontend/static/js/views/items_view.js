Sourcemash.Views.ItemsView = Backbone.View.extend({
    initialize: function(options) {
        this.listenTo(this.model, 'sync change', this.render);
        this.listenTo(this.model.items, 'sync change', this.render);
        this.itemViews = [];
    },

    render: function() {
        var content = this.template({ model: this.model });

        this.$el.html(content);

        var itemViews = [];

        var feed = (this.model.get('title') ? this.model : null);
        var items = this.model.items;
        
        items.forEach(function(item) {
            var itemCardView = new Sourcemash.Views.ItemCardView({ model: item, feed: feed || item.feed, items: items });
            $("#items").append(itemCardView.el)
            itemViews.push(itemCardView)
        })

        this.itemViews = itemViews;

        return this;
    },

    close: function() {
        this.remove();
        this.unbind();

        _.each(this.itemViews, function(itemView) {
            itemView.remove();
            itemView.unbind();
        })
    }
});
