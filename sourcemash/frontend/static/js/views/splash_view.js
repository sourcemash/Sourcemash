Sourcemash.Views.SplashView = Backbone.View.extend({
    template: JST['splash'],

    events: {
      'click #need-account': 'showRegisterModal',
    },

    showRegisterModal: function(){
      $("#register-modal").openModal();
    },

    render: function() {
        // Render footer view
        this.footerView = new Sourcemash.Views.FooterView();
        $("#sourcemash-footer").html(this.footerView.render().el);

        this.$el.html(this.template());
        return this;
    },

    close: function() {
        $("#sourcemash-footer").html("");
        this.footerView.remove();
        this.footerView.unbind();
    }
});
