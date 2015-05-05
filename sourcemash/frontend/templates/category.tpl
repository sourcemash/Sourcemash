<div class="container">
  <div class="row valign-wrapper">
      <h2 class="col s11"><%= model.get('name') %></h2>

      <span title="Mark as Read" class="mark-all-read col s1"><i class="medium mdi-action-done-all"></i></span>
  </div>

  <div class="loading center-align"></div>

  <ul id="items" class="list-group row">
    <% items.forEach(function(item) { %>
        <div id="item-<%= item.get('id') %>" class="item-card"></div>
    <% }); %>
  </ul>

  <div id="subscribe-modal" class="modal"></div>
</div>
