$( document ).ready(function(){
	$(".button-collapse").sideNav();
});

$(document).ajaxError(function (e, xhr, options) {
  var errors = xhr.responseJSON.errors;
  for (errorField in errors) {
    if (errors.hasOwnProperty(errorField)) {
        var inputField = $("#" + errorField);
        inputField.removeClass("valid");
        inputField.addClass("invalid");
        var fieldErrors = $('.' + errorField + "-errors");
        fieldErrors.text(errors[errorField]);
    }
  }
});