$( document ).ready(function(){
	$(".button-collapse").sideNav();
});

add_feed = function() {
	var feed_url = $("#feed_url").val();
	$.ajax({
		type: "POST",
		url: "/api/subscriptions",
		data: {'feed_url': feed_url},
		dataType: "json",
		success: function(data) {
			
			// var feed_string = "<p><a href=" + data.url + ">" data.title + "</a></p>"
			console.log(data)
			// $(".feeds").append(feed_string)
		}
	})
}