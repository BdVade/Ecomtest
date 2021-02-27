from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'
		
		
class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'

class ShippingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Shipping
		fields = ['order', 'address', 'city', 'state', 'zipcode']


class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'