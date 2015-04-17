Sourcemash.Views.ProfileView = Backbone.View.extend({
  template: JST['profile'],

  events: {
    "click #delete-user": 'deleteUser'
  },

  initialize: function(options) {
    this.listenTo(this.model, 'change', this.render);
  },

  render: function() {
    var content = this.template({model: this.model});
    this.$el.html(content);
    return this;
  },

  deleteUser: function() {
    this.model.destroy();
  }
});
