Sourcemash.Views.RegisterModalView = Backbone.View.extend({
    template: JST['register-modal'],

    events: {
        'submit #register': 'registerFromModal',
    },

    registerFromModal: function(e) {
        e.preventDefault();
        var formData = JSON.stringify($("#register").serializeObject());
        $('#register-password').val('');
        $('#register-password-confirm').val('');
        var posting = $.ajax({
                          type: "POST",
                          url: "/register",
                          data: formData,
                          success: this.registerOrShowErrors,
                          contentType: "application/json"
                      });
    },

    registerOrShowErrors: function(data) {
        var user = data.response.user;
        if (user) {
          mixpanel.track("Registered");
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

    render: function() {
        this.$el.html(this.template());
        return this;
    }
});
