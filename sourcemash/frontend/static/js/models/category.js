Sourcemash.Models.Category = Backbone.Model.extend({
    urlRoot: '/api/categories',

    parse: function (response) {
      if (response.category) {
          return response.category;
      };
      return response;
    }
});
