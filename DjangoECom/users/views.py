from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.urls import reverse
from DjangoECom import settings
from django.contrib.auth.models import User, auth, Group
from .models import Customer
from products.decorators import unauthenticated_user, allowed_users
from django.contrib.auth import logout as django_logout
from products.models import *
from currencies.models import Currency
import requests
# Create your views here.
def index(request):
    #Multi-currency code.
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY
    else:
        if request.user.is_authenticated:
            # Where USD is the base currency you want to use
            url = 'https://api.exchangerate-api.com/v4/latest/USD'

            # Making our request
            response = requests.get(url)
            data = response.json()
            #setting the updated factor.
            currency_code = request.user.customer.currency_id
            currency = Currency.objects.get(code=currency_code)
            currency.factor = data['rates'][currency_code]
            currency.save()

    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else: 
        cartItems = 0
    context={'cartItems':cartItems}
    return render(request, "users/index.html",context)

@unauthenticated_user
def account_view(request):
    if request.method == "POST":
        if request.POST['submit'] == 'login':
            # your sign in logic goes here
            username = request.POST["logUserName"]
            password = request.POST["logPassword"]
            #authenticate not working
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "users/account.html", {
                    "message": "Invalid credentials please sign up."
                })

        elif request.POST['submit'] == 'signup':
            # your sign up logic goes here
            firstname = request.POST["regFirstName"]
            secondname = request.POST["regLastName"]
            username = request.POST["regUserName"]
            password1 = request.POST["regPassword"]
            password2 = request.POST["regReEnteredPassword"]
            email = request.POST["regEmailAddress"]
            phone = request.POST["regPhoneNumber"]
            check = request.POST["accountType"]

            if password1 == password2:
                if (len(password1) >= 8):
                    if (len(phone) == 11) and (phone.isdigit()):
                        try:
                            user = User.objects.create_user(
                                username=username,
                                password=password1,
                                email=email,
                                first_name=firstname,
                                last_name=secondname)
                            user.save()
                            id = user.id
                        except:
                            return render(request, "users/account.html", {
                                "message": "Username already taken." 
                            })   

                        try:
                            if check == "seller":
                                group = Group.objects.get(name='seller')
                                user.groups.add(group)
                                customer = Customer.objects.create(
                                    phone=phone,
                                    isseller=True,
                                    user_id=id
                                )
                                customer.save()
                                return render(request, "users/account.html")
                            elif (check == "buyer"):
                                group = Group.objects.get(name='customer')
                                user.groups.add(group)
                                customer = Customer.objects.create(
                                    phone=phone,
                                    isseller=False,
                                    user_id=id
                                )
                                customer.save()
                                return render(request, "users/account.html")
                        except:
                            user.delete()
                            return render(request, "users/account.html", {
                                "message": "Please enter your Phone number." 
                            })
                    else:
                        return render(request, "users/account.html", {
                            "message": "Your Phone number is not correct." 
                        })                          
                else:
                    return render(request, "users/account.html", {
                        "message": "Your password must contain at least 8 characters."
                    })          
            else:
                return render(request, "users/account.html", {
                    "message": "Passwords not match"
                })
    return render(request, "users/account.html")

def logout(request):
    django_logout(request)
    return render(request, "users/account.html")

def selectcurrency(request):
    if request.method == 'POST':
        # Where USD is the base currency you want to use
        url = 'https://api.exchangerate-api.com/v4/latest/USD'

        # Making our request
        response = requests.get(url)
        data = response.json()

        currency_code = request.POST['currency']
        currency = Currency.objects.get(code=currency_code)
        currency.factor = data['rates'][currency_code]
        currency.save()
        request.session['currency'] = currency_code
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@allowed_users(allowed_roles=['customer', 'seller', 'admin'])    
def savecurrency(request):
    #Save currency to user database.
    user_data = Customer.objects.get(user_id=request.user.id)
    user_data.currency_id = request.session['currency']
    user_data.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
