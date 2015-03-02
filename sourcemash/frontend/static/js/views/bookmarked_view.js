Sourcemash.Views.BookmarkedView = Sourcemash.Views.ItemsView.extend({
    template: JST['bookmarked'],
    id: "bookmarked-items",

    initialize: function(options) {
        this.itemViews = [];
    },
});