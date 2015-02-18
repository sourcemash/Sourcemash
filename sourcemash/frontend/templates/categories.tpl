<div class="row">
    <h2>Categories</h2>
</div>

<ul class="collection categories">
  <% categories.forEach(function(category) { %>
    <a href="#/categories/<%= category.get('category') %>" class="collection-item"><%= category.get('category') %></a>
  <% }); %>
</ul>