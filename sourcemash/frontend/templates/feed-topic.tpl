<div id="<%= topic %>" class="section scrollspy topic-divider valign-wrapper">
  <h5><%= topic %></h5>
</div>
<ul class="browse-feeds row">
  <div class="col s12">
    <% if (models.length == 0) { %>
      <p><a href="#add_feed_form" id="mash-add-feeds-msg">Feeds you add</a> will be added to the Mash category!
    <% } else { %>
      <% models.forEach(function(model) { %>
        <div id="feed-card-<%= model.get('id') %>" class="feed-card"></div>
      <% }); %>
    <% }; %>
  </div>
</ul>
