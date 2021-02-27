from django.db import models
from users.models import Profile
# Create your models here.


# Model for category 
class Category(models.Model):
	name = models.CharField(max_length=150)
	slug = models.SlugField(unique=True, max_length=170)
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name

	def get_products(self):
		return self.product_set.all()

		
# Model for product
class Product(models.Model):
	product_name = models.CharField(max_length=150)
	product_description = models.TextField()
	product_slug = models.SlugField(max_length=170, unique=True, null=True)
	product_image = models.ImageField(upload_to='product_images', default='')
	product_price = models.DecimalField(max_digits=7, decimal_places=2)
	product_rating = models.DecimalField(default=0, max_digits=3, decimal_places=1)
	product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
	date_posted = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.product_name

	def get_products_comments(self):
		return self.comment_set.all()

	def get_number_of_comments(self):
		return self.comment_set.all().count()

	@property
	def imageURL(self):
		try:
			url = self.product_image.url
		except:
			url = ''
		return url



class Comment(models.Model):
	first_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50, blank=True)
	text = models.TextField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
	date_posted = models.DateTimeField(auto_now_add=True)

STATUS = (
	('pending', 'Pending'),
	('processing', 'Processing'),
	('delievered', 'Delievered'),
)

class Order(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	order_status = models.CharField(choices=STATUS, max_length=10, default='pending')
	transaction_id = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.transaction_id

	def get_cart_total(self):
		order_items = self.orderitem_set.all()
		total = sum([item.get_total for item in order_items])
		return total

	@property
	def order_items(self):
		order_items = self.orderitem_set.all()
		return order_items

	def cart_items_number(self):
		order_items = self.orderitem_set.all()
		total = sum([item.quantity for item in order_items])	
		return total


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, related_name = 'order_items')
	quantity = models.IntegerField(default=1)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		price = self.quantity * self.product.product_price
		return price

class Shipping(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, blank=True)
	address = models.CharField(max_length=200, null=True, blank=True)
	city = models.CharField(max_length=50, null=True, blank=True)
	phone_number = models.CharField(max_length=15)
	state = models.CharField(max_length=50, null=True, blank=True)
	zipcode = models.CharField(max_length=100, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
