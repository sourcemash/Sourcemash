<div class="row">
    <h2>Categories</h2>
</div>

<ul class="list-group categories">
  <% categories.forEach(function(category) { %>
    <p><a href="#/categories/<%= category.get('category') %>"><%= category.get('category') %></a></p>
  <% }); %>
</ul>