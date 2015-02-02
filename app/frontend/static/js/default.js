$( document ).ready(function(){
	$(".button-collapse").sideNav();
});

$('#add_feed_form').submit(function () {
	append_feed()
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
		success: function(data) {
			var subscription = data.subscription;
			subscription_view = "<p><a href='" + subscription.url + "'>" + subscription.title + "</a></p>";
			$(".feeds").append(subscription_view);
		}
	})
}