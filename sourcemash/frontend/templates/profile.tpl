<div class="container">

  <h3 class="col s12 light center header flow-text welcome">Welcome to your Profile!</h3>
  <p class="divider">

  <ul class="collection">
    <li class="collection-item">
      <h5>
        <span class="left-align">Current email:</span>
        <span class="right light"><%= model.get('email') %></span>
      </h5>
    </li>
    <li class="collection-item">
      <h5>
        <span class="left-align">Show unsubscribed content:</span>
        <span class="right">
          <input type="checkbox" id="toggle-unsubscribed-content" <%= model.get('show_unsubscribed_content') ? 'checked' : '' %>>
          <label class="light black-text" for="toggle-unsubscribed-content" style="font-size: 1.5rem;"><%= model.get('show_unsubscribed_content') ? 'Content Shown' : 'Content Hidden' %></label>
        </span>
      </h5>
      <div class="container valign-wrapper">
        <p class="divider">
        <p class="flow-text light"><i class="mdi-action-help" style="padding-right: 5px;"></i>Determines whether the items in a given category come exclusively from feeds that you are subscribed to ("Content Hidden") or whether categories are selected at random to contain an extra item from a feed that you are not subscribed to ("Content Shown"). The goal of this feature is to help Sourcemash introduce you to new content that you may not have seen otherwise!></p>
      </div>
    </li>
  </ul>

  <a href="/"><button type="submit" class="btn waves-effect waves-light red" id="delete-user"><i class="mdi-action-delete right"></i>Delete Your Account</button></a>
</div>
