Sourcemash.Models.Category = Backbone.Model.extend({
    urlRoot: '/api/categories',

    initialize: function() {
        this.items = new Sourcemash.Collections.CategoryItems([], {category: this});
    }
});