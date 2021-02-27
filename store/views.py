from django.shortcuts import render
from .models import Category, Product, Order, OrderItem, Comment
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from .utils import cartData
import json
from django.http import JsonResponse


# Create your views here.

# endpoint to return categories

class ApiCategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ApiProductsInCategoryListView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        qs = Category.objects.get(slug=self.kwargs['slug']).get_products()
        return qs


class ApiProductComments(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        qs = Product.objects.get(product_slug=self.kwargs['product_slug']).get_products_comments()
        return qs


@api_view(['POST'])
def post_comment(request, product_slug):
    if request.method == "POST":
        product = Product.objects.get(product_slug=product_slug)
        comment = Comment(product=product)

        serializer = CommentSerializer(comment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(data={'hello': 'hello'})


@api_view(['GET'])
def get_post_comment(request, product_slug):
    if request.method == "GET":
        try:
            product = Product.objects.get(product_slug=product_slug)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comments = product.get_products_comments()
        serializer = CommentSerializer(comments)
        return Response(serializer.data)


@api_view(['GET'])
def get_product_details(request, slug):
    try:
        product = Product.objects.get(product_slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)


@api_view(['GET'])
def cart(request):
    cartdata = cartData(request)
    if cartdata == {}:
        data = {}
    else:
        data = {
            'items': cartdata['items'],
            'order': cartdata['order'],
            'cart_items': cartdata['cart_items'],
        }
    return Response(data=data)


@api_view(['POST'])
def update_cart_for_authenticated_user(request):
    data = json.loads(request.body)
    product_slug = data['product_slug']
    action = data['action']

    profile = request.user.profile
    product = Product.objects.get(product_slug=product_slug)
    order, created = Order.objects.get_or_create(profile=profile, order_status='pending')
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quality = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quality = (orderitem.quantity - 1)
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()
    return JsonResponse('It is done', safe=False)


@api_view(['POST'])
def shipping(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        address = data['shippingDetails']['address']
        email = customer.user.email
        state = data['shippingDetails']['state']
        city = data['shippingDetails']['city']
        zipCode = data['shippingDetails']['zip']
        order, created = Order.objects.get_or_create(customer=customer, order_status='pending')
        print('hi')
    else:
        customer, order = guestOrder(request, data)
        name = data['userDetails']['name']
        email = data['userDetails']['email']
        address = data['shippingDetails']['address']
        state = data['shippingDetails']['state']
        city = data['shippingDetails']['city']
        zipCode = data['shippingDetails']['zip']

    order.transaction_id = transaction_id
    total = float(data['shippingDetails']['total'])
    if total == order.get_cart_total:
        order.order_status = 'processing'
        order.save()

    Shipping.objects.create(
        profile=profile,
        order=order,
        address=address,
        state=state,
        city=city,
        zipcode=zipCode,
    )

    # send_mail(
    # 'Order '+str(transaction_id),
    # 'Your order was received and is being processed. Thanks for shopping with us.',
    # 'moyosoreolumideobi@gmail.com',
    # [email],
    # fail_silently=False,
    # )
    # serializer = ShippingSerializer(shipping)
    return JsonResponse('Done', safe=False)
