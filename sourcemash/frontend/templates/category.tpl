<div class="container">
  <div class="row valign-wrapper">
      <h2 class="col s11"><%= model.get('name') %></h2>

      <span title="Mark as Read" class="mark-all-read col s1"><i class="medium mdi-action-done-all tooltipped" data-position="bottom" data-tooltip="Mark All as Read"></i></span>
  </div>

  <div class="loading center-align"></div>

  <div id="items" class="list-group row">
    <div class="col m6 hide-on-small-and-down">
      <% for (i = 0; i < items.length; i = i + 2) { %>
        <div id="item-<%= items[i].get('id') %>-twocol" class="item-card"></div>
      <% }; %>
    </div>

    <div class="col m6 hide-on-small-and-down">
      <% for (i = 1; i < items.length; i = i + 2) { %>
        <div id="item-<%= items[i].get('id') %>-twocol" class="item-card"></div>
      <% }; %>
    </div>

    <div class="col s12 hide-on-med-and-up">
      <% for (i = 0; i < items.length; i++) { %>
        <div id="item-<%= items[i].get('id') %>-onecol" class="item-card"></div>
      <% }; %>
    </div>
  </div>

  <div id="subscribe-modal" class="modal"></div>
</div>
