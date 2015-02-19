<h2>
  <%= category.get('category') %>
</h2>

<ul class="list-group">


  <% if (category.items.length == 0) { %>
    <div class="collection-item">
        No articles found.
    </div>
  <% }; %>

  <% category.items.each(function(item) { %>
    <div class="card-panel green lighten-4">
      <div class="card-content black-text">
        <span class="card-title">
          <span class="badge"><a href="#/categories/<%=item.get('category_1')%>"><%=item.get('category_1')%></a></span>
          <span class="badge"><a href="#/categories/<%=item.get('category_2')%>"><%=item.get('category_2')%></a></span>
          <h4><a href="<%= '#/items/' + item.get('id') %>"><%= item.get('title') %></a></h4>
        </span>
        <span class="waves-effect waves-light btn-floating red"><i class="mdi-action-thumb-down downvote"></i></span>
        <span class="waves-effect waves-light btn-floating green"><i class="mdi-action-thumb-up upvote"></i></span>
        <p><%= item.get('author') %></p>
        <p><%= item.get('text') %></p>
      </div>
    </div>
  <% }); %>
</ul>