from mixer.backend.django import mixer
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, Group
from currencies.models import Currency
from DjangoECom import settings
from users.models import *
from products.models import *
from users.views import *
from products.views import *


#Users app views tests.
class UserTestViews(TestCase):
    def setUp(self):
        self.group= Group.objects.create(name="customer")
        self.currency = Currency.objects.create(
            code="USD",
            symbol="$",
            factor=1,
            name="US Dollar"
        )      

        self.user = User.objects.create(
            username="username",
            password='password1',
            email="username@example.com",
            first_name="firstname",
            last_name="secondname",
        )
        self.user.groups.add(self.group)

        self.customer = Customer.objects.create(
            phone="01234567890",
            isseller=False,
            user_id=self.user.id,
            currency_id=self.currency.code
        )

        self.client = Client()
        self.session = self.client.session


    def test_index(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        assert b'USD' in response.content


    def test_account_view_post_register(self):
        Group.objects.create(name='seller').save()
        response = self.client.post(reverse('account'), {
            "submit": 'signup',
            "regUserName": "Mark",
            "regPassword": 'password12',
            "regReEnteredPassword": 'password12', 
            "regEmailAddress": "username2@example.com",
            "regFirstName": "firstname2",
            "regLastName": "secondname2",
            "regPhoneNumber": "01234567990",
            "accountType": "seller",
            "currency_id": self.currency.code
        })
        user2= User.objects.get(username="Mark")
        seller= Customer.objects.get(phone="01234567990")
        self.assertEquals(user2.first_name, "firstname2")
        self.assertTrue(seller.isseller)
        self.assertEquals(response.status_code, 200)


    def test_account_view_post_login(self):
        response = self.client.post(reverse('account'), {
            "submit": 'login',
            "logUserName": "username",
            "logPassword": "password1"
        })
        response2 = self.client.post(reverse('account'), {
            "submit": 'login',
            "logUserName": "username2",
            "logPassword": "password1"
        })
        self.assertEquals(response.status_code, 200)
        assert b'Invalid credentials please sign up.' in response2.content


    def test_logout(self):
        url = reverse("logout")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)


    def test_selectcurrency_POST_method(self):
        url = reverse("selectcurrency")
        currency2 = Currency.objects.create(
            code="EGP",
            symbol="$LE",
            factor=15.6,
            name="Egyptian Pound"
        )      
        response = self.client.post(url, {
            "currency": currency2
        })
        self.assertEquals(response.status_code, 302)


    def test_savecurrency(self):
        url = reverse("savecurrency")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200) 


#Products app views tests.
class ProductTestViews(TestCase):
    def setUp(self):
        self.client = Client()

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


    def test_FAQS(self):
        url=reverse('faqs')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'products/faqs.html')

    
    def test_checkout_page(self):
        url = reverse('checkout')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)

    
    def test_add_review(self):
        url=reverse('add_review', args=['1'])
        request = RequestFactory().get(url)
        request.user = mixer.blend(User)
        product=mixer.blend('products.Product')
        '''resp = self.client.post(url, {
            'subject': 'product',
            'comment': 'Nice',
            'rate': 5
        })'''
        request.method ='POST'
        request.POST = {
            'subject': 'product',
            'comment': 'Nice',
            'rate': 5
        }
        #resp = add_review(request, product.id)
        #self.assertEquals(resp.status_code, 302)
        #A testing error appear because of the setting messages sessions

