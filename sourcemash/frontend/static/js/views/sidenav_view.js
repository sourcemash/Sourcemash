Sourcemash.Views.SidenavView = Backbone.View.extend({
  template: JST['sidenav'],

  initialize: function (options) {
    this.user = options.user;
    this.feeds = options.feeds;
    this.categories = options.categories;
    this.listenTo(this.feeds, 'sync change:subscribed change:unread_count', this.render);
    this.listenTo(this.categories, 'sync change:unread_count', this.render);
  },

  events: {
    'submit': 'loginSubmit',
  },

  loginSubmit: function(e){
    e.preventDefault()

    mixpanel.track("Login", { "User": this.user.get('email') })
  },

  render: function() {
    activeTab = $(".tab .active").text().toLowerCase() || "categories"

    var content = this.template({active: activeTab, current_user: this.user, feeds: this.feeds, categories: this.categories})
    this.$el.html(content);

    $('ul.tabs').tabs();
    return this;
  },
});
