<h2>
  <%= category.get('category') %>
</h2>

<ul class="list-group">
  <% category.items.each(function(item) { %>
    <div class="card-panel green lighten-4">
      <div class="card-content black-text">
        <span class="card-title">
          <span class="badge"><a href="#/categories/<%=item.get('category_1')%>"><%=item.get('category_1')%></a></span>
          <span class="badge"><a href="#/categories/<%=item.get('category_2')%>"><%=item.get('category_2')%></a></span>
          <h4><a href="<%= '#/items/' + item.get('id') %>"><%= item.get('title') %></a></h4>
        </span>
        <p><%= item.get('author') %></p>
        <p><%= item.get('text') %></p>
      </div>
    </div>
  <% }); %>
</ul>