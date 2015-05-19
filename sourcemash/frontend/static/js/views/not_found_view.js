Sourcemash.Views.NotFoundView = Backbone.View.extend({
    template: JST['not-found'],

    render: function() {
        this.$el.html(this.template());
        return this;
    }
});
