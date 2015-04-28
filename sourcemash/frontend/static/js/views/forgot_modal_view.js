Sourcemash.Views.ForgotModalView = Backbone.View.extend({
    template: JST['forgot-modal'],

    events: {
        'submit #forgot-form': 'recoverFromModal',
        'click .forgot-close': 'activateLoginForm'
    },

    recoverFromModal: function(e) {
        e.preventDefault();
        var formData = JSON.stringify($("#forgot-form").serializeObject());
        var posting = $.ajax({
                          type: "POST",
                          url: "/reset",
                          data: formData,
                          success: this.recoverPassword,
                          contentType: "application/json"
                      });
    },

    recoverPassword: function(data) {
      $("#forgot-modal").closeModal();
      toast("Check your email for further instructions.", 3000);
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
