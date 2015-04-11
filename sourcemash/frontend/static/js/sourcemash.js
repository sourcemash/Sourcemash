//
// Sourcemash
//
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

//
// jQuery
//
// Source: http://stackoverflow.com/questions/1184624/convert-form-data-to-js-object-with-jquery
jQuery.fn._serializeObject = function() {
  var arrayData, objectData;
  arrayData = this.serializeArray();
  objectData = {};

  $.each(arrayData, function() {
    var value;

    if (this.value != null) {
      value = this.value;
    } else {
      value = '';
    }

    if (objectData[this.name] != null) {
      if (!objectData[this.name].push) {
        objectData[this.name] = [objectData[this.name]];
      }

      objectData[this.name].push(value);
    } else {
      objectData[this.name] = value;
    }
  });

  return objectData;
};
