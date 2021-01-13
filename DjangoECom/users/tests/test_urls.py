from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from users.views import *
from products.views import *

class TestUrls(SimpleTestCase):
    #Users app URLS tests.
    def test_index_url_resolves(self):
        url = reverse("index")
        self.assertEquals(resolve(url).func, index)

    def test_account_url_resolves(self):
        url = reverse("account")
        self.assertEquals(resolve(url).func, account_view)

    def test_logout_url_resolves(self):
        url = reverse("logout")
        self.assertEquals(resolve(url).func, logout)

    def test_selectcurrency_url_resolves(self):
        url = reverse("selectcurrency")
        self.assertEquals(resolve(url).func, selectcurrency)

    def test_savecurrency_url_resolves(self):
        url = reverse("savecurrency")
        self.assertEquals(resolve(url).func, savecurrency)

    def test_reset_password_url_resolves(self):
        url = reverse("reset_password")
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetView)

    def test_reset_password_sent_url_resolves(self):
        url = reverse("password_reset_done")
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_confirm_url_resolves(self):
        url = reverse("password_reset_confirm", args=['uidb64', 'token'])
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)

    def test_reset_password_complete_url_resolves(self):
        url = reverse("password_reset_complete")
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)

    #Products app URLS tests.
    def test_products_url_resolves(self):
        url = reverse("products")
        self.assertEquals(resolve(url).func, products)

    def test_cart_url_resolves(self):
        url = reverse("cart")
        self.assertEquals(resolve(url).func, cart)

    def test_checkout_url_resolves(self):
        url = reverse("checkout")
        self.assertEquals(resolve(url).func, checkout)

    def test_update_item_url_resolves(self):
        url = reverse("update_item")
        self.assertEquals(resolve(url).func, updateItem)

    def test_product_details_url_resolves(self):
        url = reverse("product_details")
        self.assertEquals(resolve(url).func, productDetails)

    def test_process_order_url_resolves(self):
        url = reverse("process_order")
        self.assertEquals(resolve(url).func, processOrder)

    def test_dashboard_url_resolves(self):
        url = reverse("dashboard")
        self.assertEquals(resolve(url).func, dashboard)

    def test_category_url_resolves(self):
        url = reverse("category")
        self.assertEquals(resolve(url).func, products)

    def test_addProductView_url_resolves(self):
        url = reverse("addProductView")
        self.assertEquals(resolve(url).func, addProductView)

    def test_editProductView_url_resolves(self):
        url = reverse("editProductView")
        self.assertEquals(resolve(url).func, editProductview)

    def test_addProduct_url_resolves(self):
        url = reverse("addProduct")
        self.assertEquals(resolve(url).func, addProduct)

    def test_profile_url_resolves(self):
        url = reverse("profile")
        self.assertEquals(resolve(url).func, profile)

    def test_faqs_url_resolves(self):
        url = reverse("faqs")
        self.assertEquals(resolve(url).func, faqs)

    def test_updateProfile_url_resolves(self):
        url = reverse("updateProfile")
        self.assertEquals(resolve(url).func, updateProfile)

    def test_update_wishlist_url_resolves(self):
        url = reverse("update_wishlist")
        self.assertEquals(resolve(url).func, UpdateWishList)

    def test_wishlist_url_resolves(self):
        url = reverse("wishlist")
        self.assertEquals(resolve(url).func, ViewWishList)

    def test_add_review_url_resolves(self):
        url = reverse("add_review", args=['1'])
        self.assertEquals(resolve(url).func, add_review)