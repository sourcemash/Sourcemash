Sourcemash.Views.SplashView = Backbone.View.extend({
    template: JST['splash'],

    events: {
      'click #need-account': 'showRegisterModal',
    },

    showRegisterModal: function(){
      $("#register-modal").openModal();
    },

    render: function() {
        this.$el.html(this.template());

        // Render footer view
        this.footerView = new Sourcemash.Views.FooterView();
        this.$("#sourcemash-footer").html(this.footerView.render().el);

        return this;
    },

    close: function() {
        this.footerView.remove();
        this.footerView.unbind();
    }
});
