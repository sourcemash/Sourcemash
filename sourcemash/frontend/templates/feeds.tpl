<div class="row">
    <form class="new-feed" id="add_feed_form">
      <div id="typeahead" class="input-field col s12 m9">
      </div>
      <div class="input-field col s12 m3">
        <button type="submit" class="btn waves-effect waves-light" name='submit'>Add Feed</button>
      </div>
    </form>
</div>

<ul class="collection feeds">
  <% feeds.forEach(function(feed) { %>
    <a href="#/feeds/<%= feed.get('id') %>" class="collection-item">
      <%= feed.get('title') %>
      <span class="badge"><%=feed.get('item_count')%></span>
        <% if (feed.get('unread_count') > 0) { %>
          <span class="new badge"><%=feed.get('unread_count')%></span>
        <% }; %>
    </a>
  <% }); %>
</ul>