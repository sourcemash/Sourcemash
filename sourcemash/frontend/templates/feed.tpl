<div class="row valign-wrapper">
    <h2 class="col s11"><%= model.get('title') %></h2>

    <div class="switch col s1">
        <label>
          <input id="subscribe-switch" type="checkbox" <%= model.get('subscribed') ? 'checked' : '' %>>
          <span class="lever"></span>
          <%= model.get('subscribed') ? 'Subscribed' : 'Unsubscribed' %>
        </label>
    </div>
</div>

<ul id="items" class="list-group row"></ul>