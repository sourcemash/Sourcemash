Sourcemash.Views.SavedView = Sourcemash.Views.ItemsView.extend({
    template: JST['saved'],
    id: "saved-items",

    initialize: function(options) {
        this.itemViews = [];
    },
});