$( document ).ready(function(){
	$(".button-collapse").sideNav();
});

$(document).ajaxError(function (e, xhr, options) {
  var data = xhr.responseJSON || {};

  // Display Errors
  var errors = data.errors || [];
  for (errorField in errors) {
    if (errors.hasOwnProperty(errorField)) {
        var inputField = $("#" + errorField);
        inputField.removeClass("valid");
        inputField.addClass("invalid");
        var fieldErrors = $('.' + errorField + "-errors");
        fieldErrors.text(errors[errorField]);
    }
  }

  // Show Modal, if Not Authenticated
  var errorStatus = xhr.status;
  if (errorStatus == 405) {
    $('#register-modal').openModal();
    mixpanel.track("Register Modal", {"URL": options.url, "data": options.data});
  };

});
