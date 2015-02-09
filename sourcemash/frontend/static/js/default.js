$( document ).ready(function(){
	$(".button-collapse").sideNav();
});

$(document).ajaxError(function (e, xhr, options) {
  var errors = xhr.responseJSON;
  for (error_field in errors) {
    if (errors.hasOwnProperty(error_field)) {
        input_field = $("#"+ error_field);
        input_field.removeClass("valid");
        input_field.addClass("invalid");
        field_errors = input_field.siblings(".errors");
        field_errors.text(errors[error_field]);
    }
  }
});

Backbone.View.prototype.close = function() {
	this.remove();
	this.unbind();
};