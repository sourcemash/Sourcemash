Sourcemash.Views.CategoriesView = Backbone.View.extend({
  template: JST['categories'],
  initialize: function () {
    this.listenTo(this.collection, 'add sync remove change', this.render);
  },
  render: function() {
  	var content = this.template({categories: this.collection.models})
  	this.$el.html(content);
  	return this;
  },
});