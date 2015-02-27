<div class="row valign-wrapper">
    <h2 class="col s10 valign"><%= model.get('title') %></h2>

    <div class="switch col s2 valign-wrapper">
        <label class="valign">
          <input id="subscribe-switch" type="checkbox" <%= model.get('subscribed') ? 'checked' : '' %>>
          <span class="lever"></span>
          <p><%= model.get('subscribed') ? 'Subscribed' : 'Unsubscribed' %></p>
        </label>
    </div>
</div>

<ul id="items" class="list-group row"></ul>