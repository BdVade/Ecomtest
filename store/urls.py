from django.urls import path
from . import views


urlpatterns = [
	path('categories/', views.ApiCategoryListView.as_view(), name='categories-list'),
	path('product/<slug>/', views.get_product_details, name='product-details'),
	path('postcomment/<product_slug>/', views.post_comment, name='post_comment'),
	path('product/comments/<product_slug>/', views.ApiProductComments.as_view(), name='get_comments'),
	path('category/<slug>/', views.ApiProductsInCategoryListView.as_view()),
	path('cart/', views.cart, name='cart'),
]
