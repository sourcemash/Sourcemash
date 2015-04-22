Sourcemash.Views.RegisterModalView = Backbone.View.extend({
    template: JST['register-modal'],

    events: {
        'submit #register': 'registerFromModal',
    },

    registerFromModal: function(e) {
        e.preventDefault();
        var formData = JSON.stringify($("#register").serializeObject());
        $('#register-password').val('');
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
          mixpanel.track("Register");
          $("#register-modal").closeModal();
          toast("Check your email for confirmation!", 5000);
        };
        var errors = data.response.errors;
        if (errors) {
          errorMsg = errors.email || errors.password || errors.rememeber || {};
          $("#register-errors").html(errorMsg);
        }
    },

    render: function() {
        this.$el.html(this.template());
        return this;
    }
});
