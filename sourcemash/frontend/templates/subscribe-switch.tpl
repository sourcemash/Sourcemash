<label class="subscribe-toggle">
	<input type="checkbox" <%= model.get('subscribed') ? 'checked' : '' %>>
	<span class="lever"></span>
	<%= model.get('subscribed') ? 'Subscribed' : 'Unsubscribed' %>
 </label>
