<h2>
  <%= feed.get('title') %>
</h2>

<ul class="list-group">
  <% feed.items.each(function(item) { %>
    <div class="card-panel blue lighten-4">
      <div class="card-content black-text">
        <span class="card-title">
          <span class="badge"><%=item.get('category_1')%></span>
          <span class="badge"><%=item.get('category_2')%></span>
          <h4><a href="<%= '#/items/' + item.get('id') %>"><%= item.get('title') %></a></h4>
        </span>
        <p><%= item.get('author') %></p>
        <p><%= item.get('text') %></p>
      </div>
    </div>
  <% }); %>
</ul>