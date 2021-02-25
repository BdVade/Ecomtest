import json
from .models import *

def cookieCart(request):
	try:
		anon_cart = json.load(request.COOKIES['cart'])
	except:
		anon_cart = {}
	items = []
	order = {'get_cart_total':0, 'get_cart_items':0}
	cart_items = order['get_cart_items']
	for i in anon_cart:
		try:
			cart_items += anon_cart[i]['quantity']
			product = Product.objects.get(id=i)
			total = (product.product_price * anon_cart[i]['quantity'])		
			order['get_cart_total'] += total
			order['get_cart_items'] += cart_items

			item = {
				'product': {
					'id': product.id,
					'product_name': product.product_name,
					'product_price': product.product_price,
					'imageURL': product.imageURL,
				},
				'quantity': anon_cart[i]['quantity'],
				'get_total': total,
			}
			items.append(item)
		except:
			pass

		return {'cartItems':cart_items, 'order':order, 'items':items}
		

def cartData(request):
	if request.user.is_authenticated:
		profile = request.user.profile
		order, created = Order.objects.get_or_create(profile=profile, order_status='pending')
		items = order.orderitem_set.all()
		cart_items = order.get_cart_items_number
	else:
		cookieData = cookieCart(request)
		cart_items = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cart_items':cart_items, 'order':order, 'items':items}	


def guestOrder(request, data):
    first_name = data['userDetails']['first_name']
    last_name = data['userDetails']['last_name']
    email = data['userDetails']['email']
    address = data['shippingDetails']['address']
    state = data['shippingDetails']['state']
    city = data['shippingDetails']['city']
    zipcode = data['shippingDetails']['zip']

    cookieData = cookieCart(request)
    items = cookieData['items']
    profle, created = Profile.objects.get_or_create(email=email)
    profile.first_name = name
    profile.save()
    order = Order.objects.create(profile=profile, order_status='pending')
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return profile, order
