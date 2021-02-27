import json
from .models import *
from .serializers import OrderSerializer,ProductSerializer

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
			serialized_product = ProductSerializer(product)
			total = (product.product_price * anon_cart[i]['quantity'])		
			order['get_cart_total'] += total
			order['get_cart_items'] += cart_items

			item = {
				'product': serialized_product.data,
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
		serialized_order = OrderSerializer(order)
		items = order.orderitem_set.all()
		cart_items = order.cart_items_number
		order = serialized_order.data
		return {'order': order,}
	else:
		cookieData = cookieCart(request)
		if cookieData is not None:
			cart_items = cookieData['cartItems']
			order = cookieData['order']
			items = cookieData['items']
			return {'cart_items': cart_items, 'order': order, 'items': items}
		else:
			return {}





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
    profile, created = Profile.objects.get_or_create(email=email)
    profile.first_name = first_name
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
