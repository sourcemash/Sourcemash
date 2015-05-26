Sourcemash.Collections.Categories = Backbone.Collection.extend({
	  model: Sourcemash.Models.Category,

    url: '/api/categories',

    initialize : function(){
      _.bindAll(this, 'fetchResults');
    },

	  parse: function(response) {
	  	return response.categories;
	  },

	  comparator: function(category) {
	  	return [!category.get('unread'), category.get('name')];
	  },

    startPolling: function(item_url) {
      $.get("/api/categorizer", {'url': item_url}, this.fetchResults);
    },

    fetchResults: function(data) {
      var callbackFn = _.bind(function(data, status, headers) {
        if (headers.status === 200){
          this.add(data.categories);
          clearInterval(poller);
        }
      }, this);

      var poller = setInterval(function() {
        $.get('/api/categorizer/results', {'job_id': data.job_id}, callbackFn)
      }, 3000);
    },
});
