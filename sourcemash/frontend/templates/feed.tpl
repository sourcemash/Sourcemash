<div class="row valign-wrapper">
    <h2 class="col s10 valign"><%= model.get('title') %></h2>

    <div class="switch subscribe-switch col s2 valign-wrapper"></div>
</div>

<ul id="items" class="list-group row">
  <% items.forEach(function(item) { %>
      <div id="item-<%= item.get('id') %>" class="item-card"></div>
  <% }); %>
</ul>

<div id="subscribe-modal" class="modal"></div>
