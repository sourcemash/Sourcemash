Sourcemash.Views.FooterView = Backbone.View.extend({
    template: JST['footer'],

    render: function() {
        this.$el.html(this.template());
        return this;
    }
});
