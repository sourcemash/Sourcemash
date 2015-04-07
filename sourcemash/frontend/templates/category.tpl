<div class="row valign-wrapper">
    <h2 class="col s10 valign"><%= model.get('category') %></h2>

    <div class="col s2">
      <button type="submit" class="btn waves-effect waves-light mark-all-read"><i class="mdi-action-done-all"></i></button>
    </div>
</div>

<ul id="items" class="list-group row">
  <% items.forEach(function(item) { %>
      <div id="item-<%= item.get('id') %>" class="item-card"></div>
  <% }); %>
</ul>

<div id="subscribe-modal" class="modal"></div>
