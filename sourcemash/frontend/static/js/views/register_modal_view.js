Sourcemash.Views.RegisterModalView = Backbone.View.extend({
    template: JST['register-modal'],

    events: {
        'submit #register': 'registerFromModal',
    },

    registerFromModal: function() {
        e.preventDefault();
        var formData = JSON.stringify($("#register").serializeObject());
        var posting = $.ajax({
                          type: "POST",
                          url: "/register",
                          data: formData,
                          success: this.showErrors,
                          contentType: "application/json"
                      });

        mixpanel.track("Register", {})
    },

    showErrors: function(data) {
        var user = data.response.user;
        if (user) {
          mixpanel.track("Sign Up");
          toast("Check your email for confirmation!", 3000);
        };
        var errors = data.response.errors;
        if (errors) {
          errorMsg = errors.email || errors.password || errors.rememeber || {};
          $("#register-errors").html(errorMsg);
          $('#register-password').val('');
        }
    },

    render: function() {
        this.$el.html(this.template());
        return this;
    }
});
