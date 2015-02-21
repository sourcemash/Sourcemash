Sourcemash.Views.ItemView = Backbone.View.extend({
    template: JST['item'],

    initialize: function(options) {
        this.render();
        this.listenTo(this.model, 'sync', this.render);
    },

    render: function() {
        var content = this.template({ item: this.model });
        $(content).appendTo(this.$el);
    }
});