<div class="col m6">
  <div class="card <%= item.get('unread') ?  '' : 'read' %>">

    <div class="card-image waves-effect waves-block waves-light">
      <img class="activator mark-read" src=<%=item.get('image_url')%>>
    </div>

    <div class="card-content">

      <div class="card-title row mark-read grey-text text-darken-4">
        <div class="col s11 activator">
          <%= item.get('title') %>
        </div>
      <div class="col s1"><i class="mdi-navigation-more-vert activator right"></i></div>
      </div>

      <div class="card-action valign-wrapper row">
        <div class="col s4"><a href="/#categories/<%=item.get('category_1')%>"><%=item.get('category_1')%></a></div>
        <div class="col s4"><a href="/#categories/<%=item.get('category_2')%>"><%=item.get('category_2')%></a></div>
        <div class="col s2">
          <div class="saved">
            <i class="mdi-action-bookmark<%= item.get('saved') ? '' : '-outline' %> small"></i>
          </div>
        </div>
        <div class="col s2 center-align" id="voting-buttons">
          <div class="vote upvote <%= item.get('vote') == 1 ?  'active' : '' %>"><i class="small mdi-navigation-expand-less"></i></div>
          <div><%= item.get('voteSum') %></div>
          <div class="vote downvote <%= item.get('vote') == -1 ?  'active' : '' %> "><i class="small mdi-navigation-expand-more"></i></div>
        </div>
      </div>

    </div>

    <div class="card-reveal">
      <span class="card-title grey-text text-darken-4">
        <i class="mdi-navigation-close right"></i>
      </span>
      <p class="flow-text"><a href="<%= item.get('link') %>"><%= item.get('title') %></a></p>
      <p class="flow-text"><%= item.get('author') %></p>
      <p class="flow-text summary"><%= item.get('summary')%></p>
    </div>
  </div>
</div>
