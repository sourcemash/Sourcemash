$( document ).ready(function(){
	$(".button-collapse").sideNav();
  $('.scrollspy').scrollSpy();
  $('.tabs-wrapper .row').pushpin();
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
  if (xhr.error().status == 401) {
    $('#register-modal').openModal();
    mixpanel.track("Register Modal", {"URL": options.url, "data": options.data});
  };

});
