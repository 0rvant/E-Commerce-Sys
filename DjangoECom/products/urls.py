from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name="products"),
    path('cart', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout"),
    path('update_item', views.updateItem, name="update_item"),
    path('product_details', views.productDetails, name="product_details"),
    path('process_order',views.processOrder, name="process_order")

]