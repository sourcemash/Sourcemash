$( document ).ready(function(){
	$(".button-collapse").sideNav();
});

Backbone.View.prototype.close = function() {
	this.remove();
	this.unbind();
};