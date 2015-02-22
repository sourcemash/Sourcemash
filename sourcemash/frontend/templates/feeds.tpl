<div class="row">
    <form class="new-feed" id="add_feed_form">
      <div class="input-field col s12 m9">
        <label>Feed URL</label>
        <input type="text" id="url">
        <div class="url-errors"></div>
      </div>
      <div class="input-field col s12 m3">
        <button type="submit" class="btn waves-effect waves-light" name='submit'>Add Feed</button>
      </div>
    </form>
</div>

<a class="waves-effect waves-light btn green darken-1" href="#/categories">Categories</a>

<ul class="collection feeds">
  <% feeds.forEach(function(feed) { %>
    <a href="#/feeds/<%= feed.get('id') %>" class="collection-item"><%= feed.get('title') %>
      <span class="badge"><%=feed.get('item_count')%></span>
    </a>
  <% }); %>
</ul>