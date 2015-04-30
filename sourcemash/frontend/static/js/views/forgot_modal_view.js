Sourcemash.Views.ForgotModalView = Backbone.View.extend({
    template: JST['forgot-modal'],

    events: {
        'click .forgot-submit': 'recoverFromModal',
        'submit #forgot-form': 'recoverFromModal',
        'keyup #forgot-email': 'processKey',
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
      $('#login-email').focus();
    },

    processKey: function(e) {
      if(e.which === 13) { // enter key
        $('#forgot-form').submit();
      };
    },

    render: function() {
        this.$el.html(this.template());
        return this;
    }
});
