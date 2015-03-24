<ul class="sidenav-element">
  <li class='logo'><a href="/" class="brand-logo">Sourcemash</a></li>

  <div class="lists">
    <div class="row">
      <div class="col s12">
        <ul class="tabs">
          <li class="tab col s6"><a class="<%= active == 'categories' ? 'active' : ''%>" href="#categories-list">Categories</a></li>
          <li class="tab col s6"><a class="<%= active == 'feeds' ? 'active' : ''%>" href="#feeds-list">Feeds</a></li>
        </ul>
      </div>
      <ul id="categories-list" class="collection col s12">
        <% categories.forEach(function(category) { %>
          <li class="row"><a href="#/categories/<%= category.get('category') %>" class="collection-item">
              <span class="col s7 truncate"><%= category.get('category') %></span>
              <span class="badge col s2"><%=category.get('count')%></span>
              <% if (category.get('unread_count') > 0) { %>
                <span class="new badge col s3"><%=category.get('unread_count')%></span>
              <% }; %>
          </a></li>
        <% }); %>
      </ul>
      <ul id="feeds-list" class="collection col s12">
        <% feeds.forEach(function(feed) { %>
          <% if (feed.get('subscribed')) { %>
            <li class="row"><a href="#/feeds/<%= feed.get('id') %>" class="collection-item">
            <span class="col s7 truncate"><%= feed.get('title') %></span>
            <span class="badge col s2"><%=feed.get('item_count')%></span>
            <% if (feed.get('unread_count') > 0) { %>
              <span class="new badge col s3"><%=feed.get('unread_count')%></span>
            <% }; %>
            </a></li>
          <% }; %>
        <% }); %>
      </ul>
    </div>
  </div>
</ul>

<div class="user-auth row">
  <ul class="sidenav-element col s12">
    <% if (current_user.get('is_authenticated')) { %>
      <li><a href="#/saved">Saved</a></li>
      <li><a href="/logout">Logout</a></li>
    <% } else { %>
      <li><a href="/login">Login</a></li>
      <li><a href="/register">Register</a></li>
    <% } %>
  </ul>
</div>
