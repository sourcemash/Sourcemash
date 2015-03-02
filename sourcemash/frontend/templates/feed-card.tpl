<div class="row">
  <a href="#/feeds/<%= model.get('id') %>" class="row">
    <div class="col s10">
      <%= model.get('title') %>
    </div>
    <div class="switch col s2 valign-wrapper">
      <label id="subscribe-switch" class="valign">
        <input type="checkbox" <%= model.get('subscribed') ? 'checked' : '' %>>
        <span class="lever"></span>
        <p><%= model.get('subscribed') ? 'Subscribed' : 'Unsubscribed' %></p>
      </label>
    </div>
  </a>
</div>