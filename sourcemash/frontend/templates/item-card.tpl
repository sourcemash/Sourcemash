<div class="col m6">
  <div class="card <%= item.get('unread') ?  '' : 'read' %> <%= item.get('feed').subscribed ? '' : 'unsubscribed'%>">
    
    <div class="card-image waves-effect waves-block waves-light">
      <img class="activator" src=<%=item.get('image_url')%>>
    </div>
    
    <div class="card-content">
      
      <div class="card-title row activator grey-text text-darken-4">
        <div class="col s11">
          <%= item.get('title') %>
        </div>  
      <div class="col s1"><i class="mdi-navigation-more-vert right"></i></div>
      </div>

      <div class="card-action valign-wrapper row">
        <div class="col s4"><a href="#/categories/<%=item.get('category_1')%>"><%=item.get('category_1')%></a></div>
        <div class="col s4"><a href="#/categories/<%=item.get('category_2')%>"><%=item.get('category_2')%></a></div>
        <div class="col s2"></div>
        <div class="col s2 center-align" id="voting-buttons">
          <div class="vote upvote <%= item.get('vote') == 1 ?  'active' : '' %>"><i class="small mdi-navigation-expand-less"></i></div>
          <div><%= item.get('voteSum') %></div>
          <div class="vote downvote <%= item.get('vote') == -1 ?  'active' : '' %> "><i class="small mdi-navigation-expand-more"></i></div>
        </div>
      </div>

    </div>
    
    <div class="card-reveal">
      <span class="card-title grey-text text-darken-4">
        <i class="mdi-navigation-close right mark-read"></i>
      </span>
      <p class="flow-text"><a href="<%= '#/items/' + item.get('id') %>"><%= item.get('title') %></a></p>
      <p class="flow-text"><%= item.get('author') %></p>
      <p class="flow-text summary"><%= item.get('summary')%></p>
    </div>
  </div>
</div>

<div class="subscribe-modal modal">
  <div class="modal-content">
    <h4>Interested?</h4>
    <p>You upvoted an item from a feed you're not subscribed to. Would you like to add this feed to your subscriptions?<p>
  </div>
  <div class="modal-footer">
    <a href="#" class="subscribe-close waves-effect waves-green btn-flat modal-action modal-close">Subscribe!</a>
    <a href="#" class="waves-effect waves-green btn-flat modal-action modal-close">I'll pass...</a>
  </div>
</div>