<div class="row">
    <h2>Categories</h2>
</div>

<ul class="collection categories">
  <% categories.forEach(function(category) { %>
    <a href="#/categories/<%= category.get('category') %>" class="collection-item">
        <%= category.get('category') %>
        <span class="badge"><%=category.get('count')%></span>
        <% if (category.get('unread_count') > 0) { %>
          <span class="new badge"><%=category.get('unread_count')%></span>
        <% }; %>
    </a>
  <% }); %>
</ul>