<div id="<%= topic %>" class="section scrollspy row">
  <div class="topic-divider valign-wrapper">
    <h5><%= topic %></h5>
  </div>
  <ul class="browse-feeds">
    <div class="col s12">
      <% if (models.length == 0) { %>
        <p>Feeds you add will be added to the Mash category!
      <% } else { %>
        <% models.forEach(function(model) { %>
          <div id="feed-card-<%= model.get('id') %>" class="feed-card"></div>
        <% }); %>
      <% }; %>
    </div>
  </ul>
</div>
