from django.test import TestCase
from users.models import User, Customer, Currency
from products.models import Product, Review, Order, OrderItem, ShippingAddress, WishList, WishListItem, Faqs

class TestModels(TestCase):
    def setUp(self):
        self.currency = Currency.objects.create(
            code="USD",
            symbol="$",
            factor=1,
            name="US Dollar"
        )
        #create 2 users.
        self.user1 = User.objects.create(
            first_name="example",
            last_name="example",
            username="username",
            email="example@example.com",
            password="example1234"
        )

        self.user2 = User.objects.create(
            first_name="example2",
            last_name="example2",
            username="username2",
            email="example2@example2.com",
            password="example21234"
        )
        #create customer account.
        self.customer = Customer.objects.create(
            user_id=self.user1.id,
            phone="01234567890",
            isseller=False,
            currency_id=self.currency.code
        )
        #create seller accont.
        self.seller = Customer.objects.create(
            user_id=self.user2.id,
            phone="01234567890",
            isseller=True,
            currency_id=self.currency.code
        )
        #create 2 products.
        self.product1 = Product.objects.create(
            name="product1",
            price=100,
            seller=self.user2,
            quantity=2,
            discount_price=90,
            description="None",
            category="Clothes"
        )
        self.product2 = Product.objects.create(
            name="product2",
            price=10,
            seller=self.user2,
            quantity=10,
            discount_price=9,
            description="None",
            category="Mobiles"
        )

    #Users app models tests.
    def test_User_details(self):
        self.assertEquals(self.user1.first_name, "example")
        self.assertEquals(self.user2.first_name, "example2")
        self.assertEquals(self.user1.username, "username")
        self.assertEquals(self.user2.username, "username2")
        self.assertTrue(self.user1.password == "example1234")
    
    def test_Customer_details(self):
        self.assertFalse(self.customer.isseller)
        self.assertTrue(self.seller.isseller)
        self.assertEquals(self.customer.user.email, "example@example.com")
        self.assertEquals(self.seller.user.username, "username2")

    def test_Currency_details(self):
        self.assertEquals(self.currency.name, "US Dollar")
        self.assertEquals(self.customer.currency.code, "USD")

    #Products app models tests.
    def test_Product_details(self):
        self.assertEquals(self.product1.label, "New")
        self.assertEquals(self.product1.category, "Clothes")
        self.assertEquals(self.product2.label, "New")
        self.assertEquals(self.product2.category, "Mobiles")
        self.assertEquals(self.product1.seller.username, "username2")
        self.assertEquals(self.product1.total_review, 0)
    
    def test_imageURL(self):
        self.assertEquals(self.product1.imageURL, '/images/empty_img.png')

    def test_Review_details(self):
        review = Review.objects.create(
            product=self.product1,
            user=self.user1,
            subject="product1",
            comment="Nice",
            rate=4
        )
        self.assertEquals(review.product.name, "product1")
        self.assertEquals(review.user.username, "username")
        self.assertEquals(review.comment, "Nice")

    def test_Order_details(self):
        order = Order.objects.create(
            customer=self.customer
        )
        self.assertEquals(order.customer.user.username, "username")

    def test_OrderItem_details(self):
        order = Order.objects.create(
            customer=self.customer
        )
        orderItem = OrderItem.objects.create(
            product=self.product1,
            order=order,
            quantity=2
        )
        self.assertEquals(orderItem.product.name, "product1")
        self.assertEquals(orderItem.order.customer.user.username, "username")
        self.assertEquals(orderItem.get_total, 200)
        self.assertEquals(orderItem.get_total_discount, 180)
        self.assertTrue(order.shipping)
        self.assertEquals(order.get_cart_items, 2)
        self.assertEquals(order.get_cart_total, 200)
        self.assertEquals(order.cart_discount, 20)

    def test_ShippingAddress_details(self):
        order = Order.objects.create(
            customer=self.customer
        )
        address = ShippingAddress.objects.create(
            customer=self.customer,
            order=order,
            address="someAddress",
            city="city",
            state="state",
            zipcode="zipcode"
        )
        self.assertEquals(address.customer.user.username, "username")
        self.assertFalse(address.order.complete)

    def test_Wishlist_details(self):
        wishlist = WishList.objects.create(
            customer=self.customer
        )
        self.assertEquals(wishlist.customer.user.username, "username")

    def test_WishlistItem_details(self):
        wishlist = WishList.objects.create(
            customer=self.customer
        )
        wishListItem = WishListItem.objects.create(
            product=self.product1,
            wishList=wishlist
        )
        self.assertEquals(wishListItem.wishList.customer.user.username, "username")
        self.assertEquals(wishListItem.product.name, "product1")

    def test_Faqs_details(self):
        q = Faqs.objects.create(
            user=self.user1,
            question="Where",
            answer="Where what!"
        )
        self.assertEquals(q.user.first_name, "example")
        self.assertEquals(q.question, "Where")
        self.assertEquals(q.answer, "Where what!")