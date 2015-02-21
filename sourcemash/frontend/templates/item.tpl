<div class="card-panel lighten-4">
  <div class="card-content black-text">
    <span class="card-title">
      <span class="badge"><a href="#/categories/<%=item.get('category_1')%>"><%=item.get('category_1')%></a></span>
      <span class="badge"><a href="#/categories/<%=item.get('category_2')%>"><%=item.get('category_2')%></a></span>
      <h4><a href="<%= '#/items/' + item.get('id') %>"><%= item.get('title') %></a></h4>
    </span>
    <span class="waves-effect waves-light btn-floating red downvote"><i class="mdi-action-thumb-down"></i></span>
    <span class="waves-effect waves-light btn-floating green upvote"><i class="mdi-action-thumb-up"></i></span>
    <p><%= item.get('author') %></p>
    <p><%= item.get('text') %></p>
  </div>
</div>