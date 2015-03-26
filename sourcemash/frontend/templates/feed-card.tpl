<div class="col m6">
  <div class="card">

    <div class="card-image waves-effect waves-block waves-light">
      <a href="/#feeds/<%= model.get('id') %>">
        <img class="activator mark-read" src=<%= model.get('image_url') %>>
      </a>
    </div>

    <div class="card-content">

      <div class="card-title">
        <div class="col s9">
          <a href="/#feeds/<%= model.get('id') %>" class="row">
            <%= model.get('title') %>
          </a>
        </div>
        <div class="switch subscribe-switch col s3 valign-wrapper"></div>
      </div>

      <div class="card-action valign-wrapper row">
        <p class="flow-text">
          <%= model.get('description') %>
        </p>
      </div>

    </div>

  </div>
</div>
