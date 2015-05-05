Sourcemash.Views.SidenavView = Backbone.View.extend({
  template: JST['sidenav'],

  initialize: function (options) {
    this.user = options.user;
    this.feeds = options.feeds;
    this.categories = options.categories;
    this.loading = true;
    this.listenTo(this.feeds, 'sync change:subscribed change:unread_count', this.render);
    this.listenTo(this.categories, 'sync change:unread_count', this.render);
  },

  events: {
    'submit #login': 'loginSubmit',
    'click #need-account': 'showRegisterModal',
    'click #forgot-password': 'showForgotPasswordModal'
  },

  loginSubmit: function(e){
    e.preventDefault();
    var formData = JSON.stringify($("#login").serializeObject());
    var posting = $.ajax({
                      type: "POST",
                      url: "/login",
                      data: formData,
                      success: this.loginUserOrShowErrors,
                      contentType: "application/json"
                  });
  },

  loginUserOrShowErrors: function(data){
    var user = data.response.user;
    if (user) {
      mixpanel.track("Logged In");
      window.location.reload(true);
      window.location.replace("/#browse");
    };
    var errors = data.response.errors;
    if (errors) {
      errorMsg = errors.email || errors.password || errors.rememeber || {};
      $("#login-errors").html(errorMsg);
      $('#password').val('');
    }
  },

  showRegisterModal: function(){
    $("#register-modal").openModal();
  },

  showForgotPasswordModal: function(){
    $("#forgot-modal").openModal();
  },

  render: function() {
    this.close();

    activeTab = $(".tab .active").text().toLowerCase() || "categories";

    var content = this.template({active: activeTab, current_user: this.user, feeds: this.feeds,
                                 categories: this.categories});
    this.$el.html(content);

    // Render loading view
    this.loadingView = new Sourcemash.Views.LoadingView({loading: this.loading});
    this.$(".loading").html(this.loadingView.render().el);

    $('ul.tabs').tabs();
    return this;
  },

  close: function() {
    if (this.loadingView) {
        this.loadingView.remove();
        this.loadingView.unbind();
    };
  }
});
