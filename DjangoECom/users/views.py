from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

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
         return render(request, "users/login.html")

    elif request.POST.get('submit') == 'sign_up':
            # your sign up logic goes here


def logout_view(request):
    pass