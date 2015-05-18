Sourcemash.Views.HelpView = Backbone.View.extend({
    template: JST['help'],

    initialize: function(options) {
        this.user = options.user;
    },

    events: {
        'click .help-fixed-action-btn': 'showHelpModal',
        'click #go-to-profile': 'showProfileOrRegisterModal',
        'click #focus-login': 'activateLoginForm',
        'click #show-register-modal': 'showRegisterModal',
    },

    showHelpModal: function() {
        $("#help-modal").openModal();
    },

    showProfileOrRegisterModal: function(e) {
        e.preventDefault();
        $("#help-modal").closeModal();
        if (this.user.get('email')) {
            window.location.href = "/#profile";
        } else {
            setTimeout(function(){$("#register-modal").openModal();}, 250);
        };
    },

    activateLoginForm: function() {
        $("#help-modal").closeModal();
        setTimeout(function(){$('#login-email').focus();}, 250);
    },

    showRegisterModal: function() {
        $("#help-modal").closeModal();
        setTimeout(function(){$("#register-modal").openModal();}, 250);
    },

    render: function() {
        this.$el.html(this.template());
        return this;
    }
});
