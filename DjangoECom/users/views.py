from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from .models import Customer,Seller

# Create your views here.
def index(request):
    return render(request, "users/index.html")


    
def account_view(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'login':
            # your sign in logic goes here
            username = request.POST["logUserName"]
            password = request.POST["logPassword"]
            check = request.Post["loguser"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "users/account.html", {
                "message": "Invalid credentials."
                })

        elif request.POST.get('submit') == 'signup':
                # your sign up logic goes here
            firstname=request.POST["regFirstName"]
            secondname=request.POST["regLastName"]
            username = request.POST["regUserName"]
            password1 = request.POST["regPassword"]
            password2 =request.POST["regReEnteredPassword"]
            email=request.POST["regEmailAddress"]
            phone=request.POST["regPhoneNumber"]
            check = request.Post["reguser"]

            if(password1 == password2):
                customer=Customer.objects.create(username=username, password=password1, phone=phone, email=email, firstname=firstname, secondname=secondname)
                customer.save()
                login(request,customer)
            else:
                return render(request, "users/account.html", {
                    "message": "Password not match"
                })
    return render(request, "users/account.html")

def logout(request):
    logout(request)
    return redirect('/')