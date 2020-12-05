from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from .models import Customer,Seller

# Create your views here.
def index(request):
    pass


    
def account_view(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'sign_in':
            # your sign in logic goes here
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
             if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "users/login.html", {
                "message": "Invalid credentials."
                })

        elif request.POST.get('submit') == 'sign_up':
                # your sign up logic goes here
            firstname=request.POST["firstname"]
            secondname=request.POST["secondname"]
            username = request.POST["username"]
            password1 = request.POST["password1"]
            password2 =request.POST["password2"]
            email=request.POST["email"]
            phone=request.POST["phone"]
            address=request.POST["address"]

            if(password1 == password2):
                customer=Customer.objects.create(username=username,password=password1,phone=phone,address=address,email=email,firstname=firstname,secondname=secondname)
                customer.save()
                login(request,customer)
            else:
                return render(request, "users/login.html", {
                    "message": "Password not match"
                })

    return render(request, "users/login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')