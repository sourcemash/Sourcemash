Sourcemash.Views.ProfileView = Backbone.View.extend({
  template: JST['profile'],

  initialize: function(options) {
    this.listenTo(this.model, 'change', this.render);
  },

  events: {
    "click #delete-user": 'deleteUser',
    "click #toggle-suggested-content": 'toggleShowSuggestedContent'
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

  toggleShowSuggestedContent: function() {
    this.model.save({'show_suggested_content': !this.model.get('show_suggested_content')},
                    {success: this.showContentToggled});
  },

  showContentToggled: function(user) {
    if (user.get('show_suggested_content')) {
      toast("Suggested content will be shown!", 3000);
      mixpanel.track("Enabled Suggested Content")
    } else {
      toast("Suggested content will no longer be shown.", 3000);
      mixpanel.track("Disabled Suggested Content")
    }
  }

});
