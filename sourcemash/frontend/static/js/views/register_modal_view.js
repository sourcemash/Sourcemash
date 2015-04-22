Sourcemash.Views.RegisterModalView = Backbone.View.extend({
    template: JST['register-modal'],

    events: {
        'submit #register': 'registerFromModal',
    },

    registerFromModal: function(e) {
        e.preventDefault();
        var formData = JSON.stringify($("#register").serializeObject());
        $('#register-password').val('');
<<<<<<< HEAD
        $('#register-password-confirm').val('');
=======
>>>>>>> register form ajax call. doesn't work locally but i have a feeling it will work on staging/production
        var posting = $.ajax({
                          type: "POST",
                          url: "/register",
                          data: formData,
                          success: this.showErrors,
                          contentType: "application/json"
                      });
    },

    showErrors: function(data) {
        var user = data.response.user;
        if (user) {
<<<<<<< HEAD
          mixpanel.track("Register", {"User": user});
=======
          mixpanel.track("Register");
>>>>>>> register form ajax call. doesn't work locally but i have a feeling it will work on staging/production
          $("#register-modal").closeModal();
          toast("Check your email for confirmation!", 5000);
        };
        var errors = data.response.errors;
        if (errors) {
          errorMsg = errors.email || errors.password || errors.password_confirm || {};
          $("#register-errors").html(errorMsg);
<<<<<<< HEAD
        };
=======
        }
>>>>>>> register form ajax call. doesn't work locally but i have a feeling it will work on staging/production
    },

    render: function() {
        this.$el.html(this.template());
        return this;
    }
});
