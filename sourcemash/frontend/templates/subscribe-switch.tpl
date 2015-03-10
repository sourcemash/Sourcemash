<label class="subscribe-toggle valign">
	<input type="checkbox" <%= model.get('subscribed') ? 'checked' : '' %>>
	<span class="lever"></span>
	<p><%= model.get('subscribed') ? 'Subscribed' : 'Unsubscribed' %></p>
 </label>