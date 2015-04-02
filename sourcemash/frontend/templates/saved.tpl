<h2>Saved</h2>

<ul id="items" class="list-group row">
  <% items.forEach(function(item) { %>
    <% if (item.get('saved')) { %>
      <div id="item-<%= item.get('id') %>" class="item-card"></div>
    <% }; %>
  <% }); %>
</ul>

<div id="subscribe-modal" class="modal">
  <div class="modal-content">
    <h4>Interested?</h4>
    <p>You saved or upvoted "<span id="unsubscribed-item-title"></span>" even though you're not subscribed to <i><span id="unsubscribed-feed-title"></span></i>. Would you like to add this feed to your subscriptions?<p>
  </div>
  <div class="modal-footer">
    <a href="#" class="subscribe-close waves-effect waves-green btn-flat modal-action modal-close">Subscribe!</a>
    <a href="#" class="waves-effect waves-green btn-flat modal-action modal-close">I'll pass...</a>
  </div>
</div>
