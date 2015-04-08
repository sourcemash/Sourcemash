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

    var formData = JSON.stringify($("#login").serializeObject());

    $.ajax({
      type: "POST",
      url: "/login",
      data: formData,
      success: function(response){
        var user = response.response.user;
        if (user) {
          location.reload();
        }
        var errors = response.response.errors;
        if (errors) {
          errorMsg = errors.email || errors.password || errors.rememeber || {};
          $("#login-errors").html(errorMsg);
          $('#email').val('');
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

// Source: http://stackoverflow.com/questions/1184624/convert-form-data-to-js-object-with-jquery
jQuery.fn.serializeObject = function() {
  var arrayData, objectData;
  arrayData = this.serializeArray();
  objectData = {};

  $.each(arrayData, function() {
    var value;

    if (this.value != null) {
      value = this.value;
    } else {
      value = '';
    }

    if (objectData[this.name] != null) {
      if (!objectData[this.name].push) {
        objectData[this.name] = [objectData[this.name]];
      }

      objectData[this.name].push(value);
    } else {
      objectData[this.name] = value;
    }
  });

  return objectData;
};
