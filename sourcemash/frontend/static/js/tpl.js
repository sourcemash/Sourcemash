window.JST = window.JST || {};
var template = function(str){var fn = new Function('obj', 'var __p=[],print=function(){__p.push.apply(__p,arguments);};with(obj||{}){__p.push(\''+str.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/<%=([\s\S]+?)%>/g,function(match,code){return "',"+code.replace(/\\'/g, "'")+",'";}).replace(/<%([\s\S]+?)%>/g,function(match,code){return "');"+code.replace(/\\'/g, "'").replace(/[\r\n\t]/g,' ')+"__p.push('";}).replace(/\r/g,'\\r').replace(/\n/g,'\\n').replace(/\t/g,'\\t')+"');}return __p.join('');");return fn;};
window.JST['categories'] = template("<div class=\"row\">\n    <h2>Categories</h2>\n</div>\n\n<ul class=\"collection categories\">\n  <% categories.forEach(function(category) { %>\n    <a href=\"#/categories/<%= category.get('category') %>\" class=\"collection-item\">\n        <%= category.get('category') %>\n        <span class=\"badge\"><%=category.get('count')%></span>\n        <% if (category.get('unread_count') > 0) { %>\n          <span class=\"new badge\"><%=category.get('unread_count')%></span>\n        <% }; %>\n    </a>\n  <% }); %>\n</ul>");
window.JST['category'] = template("<h2><%= model.get('category') %></h2>\n\n<ul id=\"items\" class=\"list-group row\"></ul>");
window.JST['feed'] = template("<div class=\"row valign-wrapper\">\n    <h2 class=\"col s10 valign\"><%= model.get('title') %></h2>\n\n    <div class=\"switch col s2 valign-wrapper\">\n        <label class=\"valign\">\n          <input id=\"subscribe-switch\" type=\"checkbox\" <%= model.get('subscribed') ? 'checked' : '' %>>\n          <span class=\"lever\"></span>\n          <p><%= model.get('subscribed') ? 'Subscribed' : 'Unsubscribed' %></p>\n        </label>\n    </div>\n</div>\n\n<ul id=\"items\" class=\"list-group row\"></ul>");
window.JST['feeds'] = template("<div class=\"row\">\n    <form class=\"new-feed\" id=\"add_feed_form\">\n      <div id=\"typeahead\" class=\"input-field col s12 m9\">\n      </div>\n      <div class=\"input-field col s12 m3\">\n        <button type=\"submit\" class=\"btn waves-effect waves-light\" name='submit'>Add Feed</button>\n      </div>\n    </form>\n</div>\n\n<a class=\"waves-effect waves-light btn green darken-1\" href=\"#/categories\">Categories</a>\n\n<ul class=\"collection feeds\">\n  <% feeds.forEach(function(feed) { %>\n    <a href=\"#/feeds/<%= feed.get('id') %>\" class=\"collection-item\">\n      <%= feed.get('title') %>\n      <span class=\"badge\"><%=feed.get('item_count')%></span>\n        <% if (feed.get('unread_count') > 0) { %>\n          <span class=\"new badge\"><%=feed.get('unread_count')%></span>\n        <% }; %>\n    </a>\n  <% }); %>\n</ul>");
window.JST['item-card'] = template("<div class=\"col m6\">\n  <div class=\"card <%= item.get('unread') ?  '' : 'read' %> <%= item.get('feed').subscribed ? '' : 'unsubscribed'%>\">\n    \n    <div class=\"card-image waves-effect waves-block waves-light\">\n      <img class=\"activator\" src=<%=item.get('image_url')%>>\n    </div>\n    \n    <div class=\"card-content\">\n      \n      <div class=\"card-title row activator grey-text text-darken-4\">\n        <div class=\"col s11\">\n          <%= item.get('title') %>\n        </div>  \n      <div class=\"col s1\"><i class=\"mdi-navigation-more-vert right\"></i></div>\n      </div>\n\n      <div class=\"card-action valign-wrapper row\">\n        <div class=\"col s4\"><a href=\"#/categories/<%=item.get('category_1')%>\"><%=item.get('category_1')%></a></div>\n        <div class=\"col s4\"><a href=\"#/categories/<%=item.get('category_2')%>\"><%=item.get('category_2')%></a></div>\n        <div class=\"col s2\"></div>\n        <div class=\"col s2 center-align\" id=\"voting-buttons\">\n          <div class=\"vote upvote <%= item.get('vote') == 1 ?  'active' : '' %>\"><i class=\"small mdi-navigation-expand-less\"></i></div>\n          <div><%= item.get('voteSum') %></div>\n          <div class=\"vote downvote <%= item.get('vote') == -1 ?  'active' : '' %> \"><i class=\"small mdi-navigation-expand-more\"></i></div>\n        </div>\n      </div>\n\n    </div>\n    \n    <div class=\"card-reveal\">\n      <span class=\"card-title grey-text text-darken-4\">\n        <i class=\"mdi-navigation-close right mark-read\"></i>\n      </span>\n      <p class=\"flow-text\"><a href=\"<%= '#/items/' + item.get('id') %>\"><%= item.get('title') %></a></p>\n      <p class=\"flow-text\"><%= item.get('author') %></p>\n      <p class=\"flow-text summary\"><%= item.get('summary')%></p>\n    </div>\n  </div>\n</div>\n\n<div class=\"subscribe-modal modal\">\n  <div class=\"modal-content\">\n    <h4>Interested?</h4>\n    <p>You upvoted an item from a feed you're not subscribed to. Would you like to add this feed to your subscriptions?<p>\n  </div>\n  <div class=\"modal-footer\">\n    <a href=\"#\" class=\"subscribe-close waves-effect waves-green btn-flat modal-action modal-close\">Subscribe!</a>\n    <a href=\"#\" class=\"waves-effect waves-green btn-flat modal-action modal-close\">I'll pass...</a>\n  </div>\n</div>");
window.JST['item'] = template("<div class=\"card\">\n  \n  <div class=\"card-image waves-effect waves-block waves-light\">\n    <img class=\"activator\" src=<%=item.get('image_url')%>>\n  </div>\n  \n  <div class=\"card-content\">\n    \n    <div class=\"card-title row activator grey-text text-darken-4\">\n      <div class=\"col s11\"><%= item.get('title') %></div>\n      <div class=\"col s1\"><i class=\"mdi-navigation-more-vert right\"></i></div>\n    </div>\n\n    <div class=\"card-action valign-wrapper row activator\">\n      <div class=\"col s5\"><a href=\"#/categories/<%=item.get('category_1')%>\"><%=item.get('category_1')%></a></div>\n      <div class=\"col s5\"><a href=\"#/categories/<%=item.get('category_2')%>\"><%=item.get('category_2')%></a></div>\n      <div class=\"col s2 center-align\" id=\"voting-buttons\">\n        <div class=\"vote upvote <%= item.get('vote') == 1 ?  'active' : '' %>\"><i class=\"small mdi-navigation-expand-less\"></i></div>\n        <div><%= item.get('voteSum') %></div>\n        <div class=\"vote downvote <%= item.get('vote') == -1 ?  'active' : '' %> \"><i class=\"small mdi-navigation-expand-more\"></i></div>\n      </div>\n    </div>\n\n  </div>\n  \n  <div class=\"card-reveal\">\n    <span class=\"card-title grey-text text-darken-4\">\n      <i class=\"mdi-navigation-close right\"></i>\n    </span>\n    <p class=\"flow-text\"><a href=\"<%= '#/items/' + item.get('id') %>\"><%= item.get('title') %></a></p>\n    <p class=\"flow-text\"><%= item.get('author') %></p>\n    <p class=\"flow-text summary\"><%= item.get('summary')%></p>\n  </div>\n\n</div>");
window.JST['new_feed_form'] = template("<label>Feed Title or URL</label>\n<input class=\"typeahead\" type=\"text\" id=\"url\">\n<ul class=\"dropdown-menu\"></ul>\n<div class=\"url-errors\"></div>");
window.JST['profile'] = template("<h2>Profile</h2>\n\n<h4 class=\"welcome\">Hello there, <%= model.get('email') %>!</h4>");
