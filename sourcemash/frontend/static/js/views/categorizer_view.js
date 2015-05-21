Sourcemash.Views.CategorizerView = Backbone.View.extend({
  template: JST['categorizer'],

  initialize: function (options) {
    this.loading = false;
    this.url = null;
    this.collection = new Sourcemash.Collections.Categories();
    this.listenTo(this.collection, 'reset', this.render);
    this.listenTo(this.collection, 'add', function() {this.loading = false; this.render();});
  },

  events: {
    'submit #category_link_form': 'categorizeLink'
  },

  categorizeLink: function(e) {
    e.preventDefault();
    this.url = $("#url").val();
    this.loading = true;
    this.collection.reset();
    this.collection.startPolling(this.url);
  },

  render: function() {
      this.$el.html(this.template({loading: this.loading, categories: this.collection, url: this.url}));

      // Render loading view
      this.loadingView = new Sourcemash.Views.LoadingView({loading: this.loading});
      this.$(".loading").html(this.loadingView.render().el);

      return this;
  }
});
