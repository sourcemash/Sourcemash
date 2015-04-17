Sourcemash.Models.User = Backbone.Model.extend({
    url: '/api/user',

    parse: function (response) {
        return response.user;
    }
});
