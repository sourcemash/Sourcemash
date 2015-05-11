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

  <ul class="browse-topics row">
    <div class="col s12 m10">
      <% topics.forEach(function(topic) { %>
        <div id="feed-topic-<%= topic %>" class="feed-topic"></div>
      <% }); %>
    </div>

    <div class="col hide-on-small-only m2">
      <div class="tabs-wrapper">
        <h5 class="contents-header grey-text text-darken-2">Topics</h5>
        <ul class="section table-of-contents">
          <% topics.forEach(function(topic) { %>
            <li><a href="#<%= topic %>"><%= topic %></a></li>
          <% }); %>
        </ul>
      </div>
    </div>
  </ul>

</div>
