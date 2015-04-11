<div class="row valign-wrapper">
    <h2 class="col s9"><%= model.get('title') %></h2>

    <span title="Mark as Read" class="mark-all-read col s1"><i class="medium mdi-action-done-all"></i></span>
    <span class="switch subscribe-switch col s2 valign"></span>
</div>

<ul id="items" class="list-group row">
  <% items.forEach(function(item) { %>
      <div id="item-<%= item.get('id') %>" class="item-card"></div>
  <% }); %>
</ul>

<div id="subscribe-modal" class="modal"></div>
