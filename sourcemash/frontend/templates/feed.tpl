<div class="row valign-wrapper">
    <h2 class="col s8 valign"><%= model.get('title') %></h2>

    <div class="col s2">
      <button type="submit" class="btn waves-effect waves-light mark-all-read"><i class="mdi-action-done-all"></i></button>
    </div>
    <div class="switch subscribe-switch col s2 valign-wrapper"></div>
</div>

<ul id="items" class="list-group row">
  <% items.forEach(function(item) { %>
      <div id="item-<%= item.get('id') %>" class="item-card"></div>
  <% }); %>
</ul>

<div id="subscribe-modal" class="modal"></div>
