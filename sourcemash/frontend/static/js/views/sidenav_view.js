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
    'click #login-submit': 'loginSubmit',
  },

  loginSubmit: function(e){
    e.preventDefault()

    var formData = JSON.stringify($("#login")._serializeObject());

    $.ajax({
      type: "POST",
      url: "/login",
      data: formData,
      success: function(data){
        var user = data.response.user;
        if (user) {
          location.reload();
        }
        var errors = data.response.errors;
        if (errors) {
          var errorMsg = errors.email || errors.password || errors.rememeber || {};
          $("#login-errors").html(errorMsg);
          $('#password').val('');
        }
        return;
      },
      contentType : "application/json"
    });
  },

  render: function() {
    activeTab = $(".tab .active").text().toLowerCase() || "categories"

    var content = this.template({active: activeTab, current_user: this.user, feeds: this.feeds, categories: this.categories})
    this.$el.html(content);

    $('ul.tabs').tabs();
    return this;
  },
});
