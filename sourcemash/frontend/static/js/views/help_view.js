Sourcemash.Views.HelpView = Backbone.View.extend({
    template: JST['help'],

    events: {
        'click .help-fixed-action-btn': 'showHelpModal',
        'click #show-register-modal': 'showRegisterModal',
    },

    showHelpModal: function() {
        $("#help-modal").openModal();
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
