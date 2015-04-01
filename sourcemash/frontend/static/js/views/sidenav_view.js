Sourcemash.Views.SidenavView = Backbone.View.extend({
  template: JST['sidenav'],

  initialize: function (options) {
    this.user = options.user;
    this.feeds = options.feeds;
    this.categories = options.categories;
    this.listenTo(this.feeds, 'sync change:subscribed change:unread_count', this.render);
    this.listenTo(this.categories, 'sync change:unread_count', this.render);
  },

  render: function() {
    activeTab = $(".tab .active").text().toLowerCase() || "categories"

    var content = this.template({active: activeTab, current_user: this.user, feeds: this.feeds, categories: this.categories})
    $('#nav-mobile').html(content);

    $('ul.tabs').tabs();
  },
});
