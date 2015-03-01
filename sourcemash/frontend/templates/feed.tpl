<div class="row valign-wrapper">
    <h2 class="col s10 valign"><%= model.get('title') %></h2>

    <div class="switch col s2 valign-wrapper">
        <label id="subscribe-switch" class="valign">
          <input type="checkbox" <%= model.get('subscribed') ? 'checked' : '' %>>
          <span class="lever"></span>
          <p><%= model.get('subscribed') ? 'Subscribed' : 'Unsubscribed' %></p>
        </label>
    </div>
</div>

<ul id="items" class="list-group row">
  <% items.sort().forEach(function(item) { %>
      <div id="item-<%= item.get('id') %>" class="item-card"></div>
  <% }); %>
</ul>

<div id="subscribe-modal" class="modal">
  <div class="modal-content">
    <h4>Interested?</h4>
    <p>You upvoted "<span id="unsubscribed-item-title"></span>" even though you're not subscribed to <i><span id="unsubscribed-feed-title"></span></i>. Would you like to add this feed to your subscriptions?<p>
  </div>
  <div class="modal-footer">
    <a href="#" class="subscribe-close waves-effect waves-green btn-flat modal-action modal-close">Subscribe!</a>
    <a href="#" class="waves-effect waves-green btn-flat modal-action modal-close">I'll pass...</a>
  </div>
</div>