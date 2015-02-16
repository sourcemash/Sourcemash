window.Sourcemash = {
    Models: {},
    Collections: {},
    Views: {},
    Routers: {},
    initialize: function() {
        new Sourcemash.Routers.AppRouter();
        Backbone.history.start();
    }
};

$(document).ready(function() {
    Sourcemash.initialize();
});