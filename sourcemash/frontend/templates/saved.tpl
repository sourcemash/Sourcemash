<h2>Saved</h2>

<ul id="items" class="list-group row">
  <% items.forEach(function(item) { %>
    <% if (item.get('saved')) { %>
      <div id="item-<%= item.get('id') %>" class="item-card"></div>
    <% }; %>
  <% }); %>
</ul>

<div id="subscribe-modal" class="modal"></div>
