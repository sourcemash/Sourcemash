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
        this.model.items.forEach(function(item) {
            var itemView = new Sourcemash.Views.ItemView({ model: item });
            $("#items").append(itemView.el)
            itemViews.push(itemView)
        })

        this.itemViews = itemViews;

        return this;
    },

    close: function() {
        this.remove();
        this.unbind();

        _.each(this.itemViews, function(itemView) {
            itemView.remove();
        })
    }
});