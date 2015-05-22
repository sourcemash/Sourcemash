<div class="container">

  <h3 class="col s12 light center header flow-text welcome">Welcome to your Profile!</h3>
  <p class="divider">

  <ul class="collection">
    <li class="collection-item">
      <h5>
        <span class="left-align">Email:</span>
        <span class="right light"><%= model.get('email') %></span>
      </h5>
    </li>
    <li class="collection-item">
      <h5>
        <span class="left-align">Suggested content:</span>
        <span class="right">
          <input type="checkbox" id="toggle-suggested-content" <%= model.get('show_suggested_content') ? 'checked' : '' %>>
          <label class="light black-text" for="toggle-suggested-content" style="font-size: 1.5rem;"><%= model.get('show_suggested_content') ? 'Enabled' : 'Disabled' %></label>
        </span>
      </h5>
      <div class="container">
        <p class="flow-text light"><i class="mdi-action-help" style="padding-right: 8px;"></i>Allow Sourcemash to display unsubscribed content you might enjoy.</p>
      </div>
    </li>
  </ul>

  <a href="/"><button type="submit" class="btn waves-effect waves-light red" id="delete-user"><i class="mdi-action-delete right"></i>Delete Your Account</button></a>
</div>
