from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Customer

# Create your views here.
def index(request):
    return render(request, "users/index.html")


def account_view(request):
    if request.method == "POST":
        if request.POST['submit'] == 'login':
            # your sign in logic goes here
            username = request.POST["logUserName"]
            password = request.POST["logPassword"]
            #authenticate not working
            user = authenticate(request, username=username, password=password)
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
            check = request.POST["reguser"]

            if password1 == password2:
                user = User.objects.create(
                    username=username,
                    password=password1,
                    email=email,
                    first_name=firstname,
                    last_name=secondname)
                user.save()
                id = user.id

                if check == "seller":

                    customer = Customer.objects.create(
                        phone=phone,
                        isseller=1,
                       # user_id=id
                    )
                    customer.save()
                    return render(request, "users/account.html")
                else:
                    customer = Customer.objects.create(
                        phone=phone,
                        isseller=0,
                        #user_id=id
                    )
                    customer.save()
                    return render(request, "users/account.html")
            else:
                return render(request, "users/account.html", {
                    "message": "Two Passwords not match"
                })
    return render(request, "users/account.html")

def logout(request):
    logout(request)
    return redirect('/')