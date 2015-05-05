<div class="container">
  <div class="row">
      <form class="new-feed" id="add_feed_form">
        <div id="typeahead" class="input-field col s12 m9">
        </div>
        <div class="input-field col s12 m3">
          <button type="submit" class="btn waves-effect waves-light" name='submit'>Add Feed</button>
        </div>
      </form>
  </div>

  <div class="loading center-align"></div>

  <ul class="browse-feeds row">
    <% models.forEach(function(model) { %>
      <div id="feed-card-<%= model.get('id') %>" class="feed-card"></div>
    <% }); %>
  </ul>

</div>
