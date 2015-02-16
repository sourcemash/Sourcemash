Sourcemash.Collections.Subscriptions = Backbone.Collection.extend({
      model: Sourcemash.Models.Feed,
      url: '/api/subscriptions',
      parse: function(response) {
        return response.subscriptions;
      },
      comparator: 'title'
});