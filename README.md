<html>
<body>
<h2>CoffeeShop REST API Documentation</h2>
<h3>URLs and Operations</h3>
<table border="1" cellpadding="1" cellspacing="1" style="width:500px;">
	<thead>
		<tr>
			<th scope="col">Operation</th>
			<th scope="col">URL</th>
			<th scope="col">Method</th>
			<th scope="col">Returns</th>
			<th scope="col">Inputs</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>create_order</td>
			<td>/orders</td>
			<td>POST</td>
			<td>Order, PaymentURL</td>
			<td>[id] [type] [cost] [additions]</td>
		</tr>
		<tr>
			<td>get_orders</td>
			<td>/orders</td>
			<td>GET</td>
			<td>Order List</td>
			<td>none</td>
		</tr>
		<tr>
			<td>get_orders_by_status</td>
			<td>/orders/{status}</td>
			<td>GET</td>
			<td>Order List</td>
			<td>none</td>
		</tr>
		<tr>
			<td>get_order</td>
			<td>/orders/{id}</td>
			<td>GET</td>
			<td>Order</td>
			<td>none</td>
		</tr>
		<tr>
			<td>update_order</td>
			<td>/orders/{id}</td>
			<td>PATCH</td>
			<td>Order</td>
			<td>[type] [cost] [additions]</td>
		</tr>
		<tr>
			<td>cancel_order</td>
			<td>/orders/{id}</td>
			<td>DELETE</td>
			<td>Order</td>
			<td>none</td>
		</tr>
		<tr>
			<td>prepare_order</td>
			<td>/orders/{id}/prepare</td>
			<td>PATCH</td>
			<td>Order</td>
			<td>none</td>
		</tr>
		<tr>
			<td>release_order</td>
			<td>/orders/{id}/release</td>
			<td>PATCH</td>
			<td>Order</td>
			<td>none</td>
		</tr>
		<tr>
			<td>make_payment</td>
			<td>/orders/{id}/payment</td>
			<td>PUT</td>
			<td>Payment</td>
			<td>[type] [amount] [card_name] [card_no] [card_expiry]</td>
		</tr>
		<tr>
			<td>get_payment</td>
			<td>/orders/{id}/payment</td>
			<td>GET</td>
			<td>Payment</td>
			<td>none</td>
		</tr>
	</tbody>
</table>

<p><strong>NOTE</strong>: multiple additions can be ordered by having multiple instances&nbsp;of&nbsp;&#39;additions&#39; in the request. For example: <em>http://127.0.0.1:5000/orders?id=1&amp;type=latte&amp;cost=4.99&amp;additions=cream&amp;additions=skimmed milk</em></p>

<h3>Example Usages:</h3>

<p>Creating an order:<br />
<em>http://127.0.0.1:5000/orders?id=1&amp;type=espresso&amp;cost=4.99&amp;additions=cream&amp;additions=skimmed milk</em></p>

<p>Getting an order&#39;s details:<br />
<em>http://127.0.0.1:5000/orders/1</em></p>

<p>Getting a list of all orders:<br />
<em>http://127.0.0.1:5000/orders</em></p>

<div>Getting a list of orders with a specific status:<br />
<em>http://127.0.0.1:5000/orders/open</em></div>

<div>&nbsp;</div>

<div>Updating an order:</div>

<div><em>http://127.0.0.1:5000/orders/1?additions=&quot;no ice&quot;</em></div>

<div><br />
Cancelling an order:</div>

<div><em>http://127.0.0.1:5000/orders/1</em></div>

<div>
<div>&nbsp;</div>

<div>Making a payment:</div>

<div><em>http://127.0.0.1:5000/orders/1/payment?type=cash&amp;amount=4.99</em></div>

<div>&nbsp;</div>

<div>Getting a payment&#39;s details:</div>

<div><em>http://127.0.0.1:5000/orders/1/payment</em></div>

<div>&nbsp;</div>

<div>Preparing an order (for Barristers only)</div>

<div><em>http://127.0.0.1:5000/orders/1/prepare</em></div>

<div>&nbsp;</div>

<div>Releasing an order (for Barristers only)<br />
<em>http://127.0.0.1:5000/orders/1/release</em></div>
</div>

<h3>Data Elements</h3>

<p><strong>id</strong><br />
unique identifier for orders</p>

<p><strong>status</strong><br />
the status of an order (&#39;open&#39;, &#39;preparing&#39; or &#39;released&#39;)</p>

<p><strong>type</strong><br />
the type of coffee when used in a order request (&#39;latte&#39;, &#39;espresso&#39;, &#39;black&#39;, etc) or payment type when in a payment request (&#39;cash&#39; or &#39;card&#39;)</p>

<p><strong>cost</strong><br />
the cost of the coffee being ordered</p>

<p><strong>additions</strong><br />
the additions of the coffee being ordered</p>

<p><strong>amount</strong><br />
the amount being paid in a payment</p>

<p><strong>card_name</strong><br />
the name of the card holder in a card payment</p>

<p><strong>card_no</strong><br />
the number of the card in a card payment</p>

<p><strong>card_expiry</strong><br />
the expiry date of the card in a card payment</p>
</body>
</html>
