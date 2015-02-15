<div class="row">
    <form class="new-feed" id="add_feed_form">
      <div class="input-field col s12 m9">
        <label>Feed URL</label>
        <input type="text" id="url">
        <div class="errors"></div>
      </div>
      <div class="input-field col s12 m3">
        <button type="submit" class="btn waves-effect waves-light" name='submit'>Add Feed</button>
      </div>
    </form>
</div>

<ul class="list-group feeds">
  <% feeds.forEach(function(feed) { %>
    <p><a href="#/feeds/<%= feed.get('id') %>"><%= feed.get('title') %></a></p>
  <% }); %>
</ul>