from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User, auth
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
            check = request.POST["reguser"]

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

                                customer = Customer.objects.create(
                                    phone=phone,
                                    isseller=True,
                                    user_id=id
                                )
                                customer.save()
                                return render(request, "users/account.html")
                            else:
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
    logout(request)
    return redirect('/')