<div class="card">
  
  <div class="card-image waves-effect waves-block waves-light">
    <img class="activator" src=<%=item.get('image_url')%>>
  </div>
  
  <div class="card-content">
    
    <div class="card-title grey-text text-darken-4">
      <%= item.get('title') %>
    </div>

    <div class="card-action activator">
      <a href="#/categories/<%=item.get('category_1')%>"><%=item.get('category_1')%></a>
      <a href="#/categories/<%=item.get('category_2')%>"><%=item.get('category_2')%></a>
      <a><i class="mdi-navigation-more-vert right grey-text text-darken-4" id="reveal-button"></i></a>
    </div>

  </div>
  
  <div class="card-reveal">
    <span class="card-title grey-text text-darken-4">
      <i class="mdi-navigation-close right"></i>
    </span>
    <p class="flow-text"><a href="<%= '#/items/' + item.get('id') %>"><%= item.get('title') %></a></p>
    <div id="voting-buttons">
      <span class="waves-effect waves-light btn-floating vote downvote <%= item.get('vote') == -1 ?  'active' : '' %> "><i class="mdi-action-thumb-down"></i></span>
      <span><%= item.get('voteSum') %></span>
      <span class="waves-effect waves-light btn-floating vote upvote <%= item.get('vote') == 1 ?  'active' : '' %>"><i class="mdi-action-thumb-up"></i></span>
    </div>

    <p class="flow-text"><%= item.get('author') %></p>
    <p class="flow-text">
      One common flaw we've seen in many frameworks is a lack of support for truly responsive text. While elements on the page resize fluidly, text still resizes on a fixed basis. To ameliorate this problem, for text heavy pages, we've created a class that fluidly scales text size and line-height to optimize readability for the user. Line length stays between 45-80 characters and line height scales to be larger on smaller screens.
    </p>
  </div>

</div>