<div id="splash">
  <div class="section no-pad-bot" id="splash-banner">
    <div class="container">
      <div class="row center">
      <h4 class="header col s12 light center">Categorize any link!</h4>
      </div>
      <div class="row center">
        <form id="category_link_form">
          <div class="input-field col offset-s2 s8">
            <input placeholder="e.g. http://www.cnn.com/2014/03/27/world/ebola-virus-explainer/" id="url" type="text" class="validate">
            <div class="url-errors"></div>
          </div>
          <div class="input-field col offset-s4 s4">
            <button type="submit" class="btn waves-effect waves-light" name='submit'>Categorize!</button>
          </div>
        </form>
      </div>
      <br>
      <% if (url) { %>

        <% if (categories.length == 0) { %>
          <h5 class="light">Categories for <a href="<%= url %>" class="categorizer-url" target="_blank">your link</a> are being generated...</h5>
        <% } else { %>
          <h5 class="light">Categories for <a href="<%= url %>" class="categorizer-url" target="_blank">your link</a>:</h5>
        <% } %>

        <div class="loading center-align"></div>

        <div class="row">
          <% categories.each(function(category){ %>
            <div class="col s12 m6">
              <div class="card-panel categorizer-card">
                <% if (category.get('id')) { %>
                  <a class="white-text" href="/#categories/<%= category.get('id') %>"><%= category.get('name') %></a>
                <% } else { %>
                  <span class="white-text"><%= category.get('name') %></span>
                <% } %>
              </div>
            </div>
          <% }); %>
        </div>

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
            <i class="mdi-action-shopping-basket promo-icon"></i>
          </div>
        </div>
        <div class="col s8">
          <p class="promo-caption">1. Bag-O-Words</p>
          <p class="light">First, we extract the most common phrases from the full text of the page. This is a simple tally for each occurence. Then the counts are weighted depending on our set of heuristics (i.e. Does the phrase appear in the title? Is it more than one word?).</p>
        </div>
      </div>

      <div class="row">
        <div class="col s8">
          <p class="promo-caption">2. Normalize the Data</p>
          <p class="light">Second, we use the Wikipedia API to assign articles to each phrase from Step 1. If a phrase has more than one meaning, we use its disambiguation page on Wikipedia to find the best choice. We score the relatedness of each possible article to determine which fits best.</p>
        </div>
        <div class="col s4">
          <div class="center promo">
            <i class="mdi-action-spellcheck promo-icon"></i>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col s4">
          <div class="center promo">
            <i class="mdi-image-grain promo-icon"></i>
          </div>
        </div>
        <div class="col s8">
            <p class="promo-caption">3. Cluster the Categories</p>
            <p class="light">Last, we use the relatedness metric from Step 2 to create a graph of the Wikipedia articles where the relatedness metric serves as the edge weights. This generates a group of communities. We find the densest cluster and use all of its keywords to categorize the article.</p>
        </div>
      </div>

    </div>
  </div>
  <div id="sourcemash-footer"></div>
</div>
