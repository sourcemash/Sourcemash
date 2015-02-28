Sourcemash.Models.User = Backbone.Model.extend({
    urlRoot: '/api/user',

    parse: function (response) {
        return response.user;
    }
});