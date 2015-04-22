Sourcemash.Views.LoadingView = Backbone.View.extend({
  template: JST['loading'],

  initialize: function(options) {
    this.loading = options.loading;
  },

  render: function() {
    this.$el.html(this.template({isLoading: this.loading}));
    return this;
  }
});
