Sourcemash.Views.ProfileView = Backbone.View.extend({
  template: JST['profile'],

  initialize: function(options) {
    this.listenTo(this.model, 'change', this.render);
  },

  events: {
    "click #delete-user": 'deleteUser',
    "click #toggle-unsubscribed-content": 'toggleShowUnsubscribedContent'
  },

  render: function() {
    var content = this.template({model: this.model});
    this.$el.html(content);
    return this;
  },

  deleteUser: function() {
    this.model.destroy();
    mixpanel.track("Deleted account");
  },

  toggleShowUnsubscribedContent: function() {
      if (this.model.get('show_unsubscribed_content')) {
          this.model.save({'show_unsubscribed_content': false}, {success: this.showContentToggled});
      } else {
          this.model.save({'show_unsubscribed_content': true}, {success: this.showContentToggled});
      };
  },

  showContentToggled: function(user) {
    if (user.get('show_unsubscribed_content')) {
      toast("Unsubscribed content will be shown!", 3000);
      mixpanel.track("Unsubscribed Content - On")
    } else {
      toast("Unsubscribed content will no longer be shown.", 3000);
      mixpanel.track("Unsubscribed Content - Off")
    }
  }

});
