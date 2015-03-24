Sourcemash.Views.SidenavView = Backbone.View.extend({
  template: JST['sidenav'],

  initialize: function (options) {
    this.user = options.user;
    this.feeds = options.feeds;
    this.categories = options.categories;
    this.listenTo(this.feeds, 'sync', this.render);
    this.listenTo(this.categories, 'sync', this.render);
  },

  render: function() {
    var content = this.template({current_user: this.user, feeds: this.feeds, categories: this.categories})
    this.$el.html(content);

    $('ul.tabs').tabs();

    return this;
  },
});
