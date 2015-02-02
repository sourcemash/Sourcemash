$( document ).ready(function(){
	$(".button-collapse").sideNav();
});

$('#add_feed_form').submit(function () {
	$("#feed_url").siblings(".errors").text("")
	$("#feed_url").blur()
	append_feed()
	$("#feed_url").val("");
	return false;
})

append_feed = function() {
	$.ajax({
		type: "POST",
		url: "/api/subscriptions",
		data: {
			feed_url : $("#feed_url").val()
		},
		dataType: "json",
		error: function(data, textStatus, errorThrown) {
			errors = data.responseJSON.errors
			for (field in errors) {
				input_field = $("#"+ field)
				input_field.removeClass("valid");
				input_field.addClass("invalid");
				field_errors = input_field.siblings(".errors")
				field_errors.text(errors[field])
			}
		},
		success: function(data) {
			var subscription = data.subscription;
			subscription_view = "<p><a href='" + subscription.url + "'>" + subscription.title + "</a></p>";
			$(".feeds").append(subscription_view);
		}
	})
}