<div id="splash">
  <div class="section no-pad-bot" id="splash-banner">
    <div class="container">
      <div class="row center">
      <h4 class="header col s12 light center">Categorize any link!</h4>
      </div>
      <div class="row center">
        <form id="category_link_form">
          <div class="input-field col s8">
            <input id="url" type="text" class="validate">
            <label for="url">Article Link</label>
            <div class="url-errors"></div>
          </div>
          <div class="input-field col s3">
            <button type="submit" class="btn waves-effect waves-light" name='submit'>Categorize!</button>
          </div>
        </form>
      </div>
      <br>
      <% if (url) { %>
        <h5>Categories for '<%= url %>'</h5>
        <div class="loading center-align"></div>
        <ol>
        <% categories.each(function(category){ %>
          <% if (category.get('id')) { %>
            <a href="/#categories/<%= category.get('id') %>"><li><%= category.get('name') %></li></a>
          <% } else { %>
            <li><%= category.get('name') %></li>
          <% } %>
        <% }); %>
        </ol>
      <% } %>
    </div>
    <div id="splash-divider"></div>
  </div>
  <div class="section no-pad-bot" id="splash-info">
    <div class="container">
      <div class="row">

        <h3 class="col s12 light center header flow-text" id="splash-subtitle">How does this work?</h3>

      </div>

      <div class="row">
        <div class="col s4">
          <div class="center promo">
            <i class="mdi-editor-insert-comment promo-icon"></i>
          </div>
        </div>
        <div class="col s8">
          <p class="promo-caption">Choose your sources.</p>
          <p class="light">Read the sources you want to read. Select from <a href="/#browse">our list of feeds</a>, or add your own! We categorize your news, not someone else's.</p>
        </div>
      </div>

      <div class="row">
        <div class="col s8">
          <p class="promo-caption">Categorize the news.</p>
          <p class="light">Our algorithm analyzes each article to find the categories that best match. We've done most of the heavy lifting, so you can find articles in the topic you're looking for faster.</p>
        </div>
        <div class="col s4">
          <div class="center promo">
            <i class="mdi-image-grain promo-icon"></i>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col s4">
          <div class="center promo">
            <i class="mdi-content-sort promo-icon"></i>
          </div>
        </div>
        <div class="col s8">
            <p class="promo-caption">Read by topic, browse by feed.</p>
            <p class="light">Customize your news reading experience to make Sourcemash work for you. We are also always <a href="mailto:support@sourcemash.com">open to feedback</a> and can <a href="mailto:support@sourcemash.com">answer any questions</a> that you may have.</p>
        </div>
      </div>

    </div>
  </div>
  <div id="sourcemash-footer"></div>
</div>
