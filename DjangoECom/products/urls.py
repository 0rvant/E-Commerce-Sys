from django.urls import path
from . import views
from users import views as usersview

urlpatterns = [
    path('', views.products, name="products"),
    path('cart', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout"),
    path('update_item', views.updateItem, name="update_item"),
    path('product_details', views.productDetails, name="product_details"),
    path('process_order',views.processOrder, name="process_order"),
    path('dashboard',views.dashboard, name="dashboard"),

    path('addProductView', views.addProductView, name="addProductView"),
    path('editProductView', views.editProductview, name="editProductView"),

    path('addProduct',views.addProduct, name="addProduct"),

    path('logout',usersview.logout, name="logout")

]