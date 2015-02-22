<div class="card">
  
  <div class="card-image waves-effect waves-block waves-light">
    <img class="activator" src=<%=item.get('image_url')%>>
  </div>
  
  <div class="card-content">
    
    <div class="card-title activator grey-text text-darken-4">
      <%= item.get('title') %>
      <i class="mdi-navigation-unfold-more right"></i>
    </div>

    <div class="card-action valign-wrapper row activator">
      <div class="col s5"><a href="#/categories/<%=item.get('category_1')%>"><%=item.get('category_1')%></a></div>
      <div class="col s5"><a href="#/categories/<%=item.get('category_2')%>"><%=item.get('category_2')%></a></div>
      <div class="col s2 center-align" id="voting-buttons">
        <div class="vote upvote <%= item.get('vote') == 1 ?  'active' : '' %>"><i class="small mdi-navigation-arrow-drop-up"></i></div>
        <div><%= item.get('voteSum') %></div>
        <div class="vote downvote <%= item.get('vote') == -1 ?  'active' : '' %> "><i class="small mdi-navigation-arrow-drop-down"></i></div>
      </div>
    </div>

  </div>
  
  <div class="card-reveal">
    <span class="card-title grey-text text-darken-4">
      <i class="mdi-navigation-close right"></i>
    </span>
    <p class="flow-text"><a href="<%= '#/items/' + item.get('id') %>"><%= item.get('title') %></a></p>
    <p class="flow-text"><%= item.get('author') %></p>
    <p class="flow-text summary"><%= item.get('summary')%></p>
  </div>

</div>