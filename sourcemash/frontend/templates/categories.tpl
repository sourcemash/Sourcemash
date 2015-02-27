<div class="row">
    <h2>Categories</h2>
</div>

<ul class="collection categories">
  <% categories.forEach(function(category) { %>
    <a href="#/categories/<%= category.get('category') %>" class="collection-item">
        <%= category.get('category') %>
        <span class="badge"><%=category.get('count')%></span>
        <span class="<%= category.get('unread_count') > 0 ? 'new badge' : '' %>">
        <% if (category.get('unread_count') > 0) { %>
          <%=category.get('unread_count')%>
        <% }; %>
    </a>
  <% }); %>
</ul>