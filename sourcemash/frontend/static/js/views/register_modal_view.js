Sourcemash.Views.RegisterModalView = Backbone.View.extend({
    template: JST['register-modal'],

    events: {
        'submit #register': 'registerFromModal',
        'click .register-close': 'activateLoginForm'
    },

    registerFromModal: function(e) {
        e.preventDefault();
        var formData = JSON.stringify($("#register").serializeObject());
        $('#register-password').val('');
        var posting = $.ajax({
                          type: "POST",
                          url: "/register",
                          data: formData,
                          success: this.registerUserOrShowErrors,
                          contentType: "application/json"
                      });
    },

    registerUserOrShowErrors: function(data) {
        var user = data.response.user;
        if (user) {
          mixpanel.track("Created Account");
          $("#register-modal").closeModal();
          toast("Check your email for confirmation!", 2000);
          setTimeout(function(){window.location.replace("/")}, 2000);
        };
        var errors = data.response.errors;
        if (errors) {
          errorMsg = errors.email || errors.password || {};
          $("#register-errors").html(errorMsg);
        };
    },

    activateLoginForm: function() {
      toast("<-- Login over there!", 3000)
      $('#login-email').focus();
    },

    render: function() {
        this.$el.html(this.template());
        return this;
    }
});
