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
    <div class="col s12 m10 l10">
      <% models.forEach(function(model) { %>
        <div id="feed-card-<%= model.get('id') %>" class="feed-card"></div>
      <% }); %>
    </div>

    <div class="col hide-on-small-only m2 l2">
      <h5 class="grey-text text-darken-2">Topics</h5>
      <ul class="section table-of-contents">
        <li><a href="#browse">Technology</a></li>
        <li><a href="#browse">Finance</a></li>
        <li><a href="#browse">Gaming</a></li>
        <li><a href="#browse">Business</a></li>
        <li><a href="#browse">Fashion</a></li>
      </ul>
    </div>
  </ul>

</div>
