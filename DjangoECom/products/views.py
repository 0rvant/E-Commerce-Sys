
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from .models import Product,User,OrderItem,Order,ShippingAddress
from users.models import Customer
from .decorators import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from products.models import *
from currencies.models import Currency
from django.contrib import messages
from django.forms import ModelForm
import requests
import datetime
from datetime import timezone

# Create your views here.
def index(request):
    return render(request, "users/index.html")
def faqs(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
        faqs=Faqs.objects.all()
        context = {'cartItems': cartItems,'faqs':faqs}
    else:
        faqs=Faqs.objects.all()
        items=[]
        order={'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        cartItems=order['get_cart_items']
        context = {'cartItems': cartItems, 'faqs': faqs}
    return render(request, "products/faqs.html", context)
def products(request):  #Products_Store
    categories=['Clothes','Mobiles','TVs','VideoGamesAndConsols','PC']
    category=request.GET.get('productsCategory')
    if(category in categories):
        products_list = Product.objects.filter(category=category)
    else:
        products_list = Product.objects.all()

    for product in products_list:
        #Calculate the average rate for the product.
        reviews=Review.objects.filter(product_id=product.id)
        if len(reviews)!=0:
            product.total_review = 0
            for review in reviews:
                product.total_review+=review.rate
            product.total_review/=len(reviews)
        else:
            product.total_review = 0
        diff = (datetime.datetime.now(timezone.utc) - product.date_created).total_seconds()
        if (diff > 172800) & (product.label == "New"):
            product.label = "Standard"
        product.save()

    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        cartItems=order['get_cart_items']
    # Paginator for products 
    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 8) #number of products in one page = 8
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products_list = paginator.page(paginator.num_pages)

    currency_code = request.session['currency']
    currency = Currency.objects.get(code=currency_code)
    #we need to send all Category here to choose one form them in forntend
    context = {'products':products, 'cartItems':cartItems, 'currency':currency,'categories':categories}
    return render(request, 'products/products.html', context)

def productDetails(request):  #Products_Store
    productId=request.GET['productId']
    product=Product.objects.get(id=productId)
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    category=product.category
    recommended=Product.objects.filter(category=category)
    currency_code = request.session['currency']
    currency = Currency.objects.get(code=currency_code)
    reviews=Review.objects.filter(product_id=productId, status='True')
    #we need to send all Category here to choose one form them in forntend
    context = {'product':product, 'cartItems':cartItems, 'currency':currency,'products':recommended, 'reviews':reviews}
    return render(request, 'products/productDetails.html', context)

#@allowed_users(allowed_roles=['customer'])
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    currency_code = request.session['currency']
    currency = Currency.objects.get(code=currency_code)
    context ={'items':items , 'order':order, 'cartItems':cartItems, 'currency':currency}
    return render(request, 'products/cart.html',context)

@allowed_users(allowed_roles=['customer'])
def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'products/checkout.html', context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created =Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1 )
    elif action == 'delete':
        orderItem.quantity = (orderItem.quantity - orderItem.quantity)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Done', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
        message = 'Payment Failed'
    if(customer.new==True):
         if total == order.get_cart_total_discount:
            order.complete = True
            message='Payment Succeeded'
            customer.new=False
            customer.save()
    else:
        if total == order.get_cart_total:
            order.complete = True
            message='Payment Succeeded'
            customer.new = False
            customer.save()
    order.save()

    return JsonResponse(message, safe=False)

def dashboard(request):  #Products_Store
    seller=request.user
    products=seller.product_set.all()
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        cartItems=order['get_cart_items']
    currency_code = request.session['currency']
    currency = Currency.objects.get(code=currency_code)
    context = {'products':products,'seller':seller, 'currency':currency, 'cartItems': cartItems}
    return render(request, 'products/sellerDashboard.html', context)




def addProductView(request):  #Products_Store
    seller=request.user
    productId = "null"
    context = {'seller': seller,"productId":productId}
    return render(request, 'products/addProduct.html', context)

def editProductview(request):  #Products_Store
    productId=request.GET['productId']
    seller = request.user
    context = {'seller': seller,'productId':productId}
    return render(request, 'products/addProduct.html', context)

def addProduct(request):  #Products_Store
    productId=request.POST['productId']

    uploaded_file=request.FILES['Productimg']
    fs=FileSystemStorage()
    fs.save(uploaded_file.name,uploaded_file)
    image = uploaded_file.name

    seller=request.user
    name = request.POST["productName"]
    quantity = request.POST["Quantity"]
    price = request.POST["Price"]
    discount_price = request.POST["discountPercentage"]
    description=request.POST["Description"]
    category = request.POST["category"]
    if(productId=="null"):

        product = Product.objects.create(
            name=name,
            price=price,
            quantity=quantity,
            discount_price=discount_price,
            description=description,
            image=image,
            category=category,
            seller=seller
        )
        product.save()
    else:
        Product.objects.filter(id=productId).update(
            name=name,
            price=price,
            quantity=quantity,
            discount_price=discount_price,
            description=description,
            image=image,
            category=category,
            seller=seller
        )

    products = seller.product_set.all()
    currency_code = request.session['currency']
    currency = Currency.objects.get(code=currency_code)
    context = {'products':products,'seller':seller, 'currency':currency}
    return render(request, 'products/sellerDashboard.html', context)

def profile(request):
    user=request.user
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        cartItems=order['get_cart_items']
    context = {'user': user, 'cartItems': cartItems}
    return render(request,'products/profile.html', context)

def updateProfile(request):
    customer=request.user.customer
    customerId=customer.id

    if request.POST['submit'] == 'editimg':
        uploaded_file = request.FILES['profileImg']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        image = uploaded_file.name
        Customer.objects.filter(id=customerId).update(
            image=image,
        )
    else:
        firstname = request.POST["regFirstName"]
        secondname = request.POST["regLastName"]
        username = request.POST["regUserName"]
        email = request.POST["regEmailAddress"]
        phone = request.POST["regPhoneNumber"]

        Customer.objects.filter(id=customerId).update(
            username=username,
            email=email,
            first_name=firstname,
            last_name=secondname,
            phone=phone,
        )
    customer.save()
    user=request.user
    context = {'user': user}
    return render(request,'products/profile.html', context)


def UpdateWishList(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    wishList, created =WishList.objects.get_or_create(customer=customer)

    wishListItem, created = WishListItem.objects.get_or_create(wishList=wishList,product=product)

    if action == 'add':
        wishListItem.save()
    elif action == 'delete':
        wishListItem.delete()
    return JsonResponse('Done', safe=False)

def ViewWishList(request):
    customer = request.user.customer
    wishList,created = WishList.objects.get_or_create(customer=customer)
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cartItems=0
    items =wishList.wishlistitem_set.all()
    context ={'items':items , 'wishList':wishList, 'cartItems':cartItems}
    return render(request, 'products/wishlist.html',context)

class ReviewForm(ModelForm):
    class Meta:
        model = Review 
        fields = ['subject', 'comment', 'rate']

def add_review(request, id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = Review()
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            user = request.user
            data.user_id = user.id
            data.save()
            
            messages.success(request, "Your review has been sent. Thank you for your interest.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 