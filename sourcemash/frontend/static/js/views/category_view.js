Sourcemash.Views.CategoryView = Backbone.View.extend({
    template: JST['category'],

    initialize: function(options) {
        this.listenTo(this.model, 'sync', this.render);
        this.listenTo(this.model.items, 'sync', this.render);
    },

    render: function() {
        var content = this.template({ category: this.model });
        this.$el.html(content);
        return this;
    }
});