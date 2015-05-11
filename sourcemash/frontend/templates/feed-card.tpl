<div class="col m6">
  <div class="card">

    <div class="card-image waves-effect waves-block waves-light">
      <a href="/#feeds/<%= model.get('id') %>">
        <img class="activator mark-read" src=<%= model.get('image_url') %>>
      </a>
    </div>

    <div class="card-content">

      <div class="card-title row">
        <div class="col s8">
          <a href="/#feeds/<%= model.get('id') %>">
            <%= model.get('title') %>
          </a>
        </div>
        <div class="switch subscribe-switch col s4"></div>
      </div>

      <div class="card-action valign-wrapper">
        <p class="flow-text description">
          <%= model.get('description') %>
        </p>
      </div>

    </div>

  </div>
</div>
