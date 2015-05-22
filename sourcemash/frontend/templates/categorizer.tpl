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
