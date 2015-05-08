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
    <div class="col s12 m10 l10">
      <% models.forEach(function(model) { %>
        <div id="feed-topic-<%= model.topic %>" class="feed-topic"></div>
      <% }); %>
    </div>

    <div class="col hide-on-small-only m2 l2">
      <div class="tabs-wrapper">
        <h5 class="contents-header grey-text text-darken-2">Topics</h5>
        <ul class="section table-of-contents">
          <li><a href="#Technology">Technology</a></li>
          <li><a href="#Business">Business</a></li>
          <li><a href="#Food">Food</a></li>
          <li><a href="#World">World</a></li>
          <li><a href="#Gaming">Gaming</a></li>
          <li><a href="#Fashion">Fashion</a></li>
          <li><a href="#Photography">Photography</a></li>
          <li><a href="#Comics">Comics</a></li>
          <li><a href="#Science">Science</a></li>
          <li><a href="#Finance">Finance</a></li>
          <li><a href="#Mash">Mash</a></li>
        </ul>
      </div>
    </div>
  </ul>

</div>
