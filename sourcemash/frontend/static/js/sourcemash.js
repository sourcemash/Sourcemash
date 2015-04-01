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

/* Overwrite sync to handle only attributes that have changed */
var OriginalBackboneSync = Backbone.sync;
Backbone.sync = function(method, model, options) {
  if (!options.data && model && method === 'update') {
    options.contentType = 'application/json';
    options.data = JSON.stringify(model.changedAttributes() || {});
    if (options.data === "{}") {
      return
    };
  }

  return OriginalBackboneSync.apply(this, arguments);
};

$(document).ready(function() {
    Sourcemash.initialize();
});
