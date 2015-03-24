Sourcemash.Views.SidenavView = Backbone.View.extend({
  template: JST['sidenav'],

  initialize: function (options) {
    this.user = options.user;
    this.feeds = options.feeds;
    this.categories = options.categories;
    this.active = 'categories';
    this.listenTo(this.feeds, 'sync change:unread_count', this.render);
    this.listenTo(this.categories, 'sync change:unread_count', this.render);
  },

  events: {
    "click .tab": "toggleTab"
  },

  toggleTab: function(e) {
    this.active = e.target.text.toLowerCase();
  },

  render: function() {
    var content = this.template({active: this.active, current_user: this.user, feeds: this.feeds, categories: this.categories})
    this.$el.html(content);

    $('ul.tabs').tabs();

    return this;
  },
});
