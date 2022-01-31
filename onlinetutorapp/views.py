from unittest import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from .forms import FormUser

# Create your views here.
# request -> response
# request handler / action
# Lau Wan Jing: https://itsourcecode.com/free-projects/python-projects/django-login-and-registration-with-source-code/
# Lau Wan Jing: https://ordinarycoders.com/blog/article/django-user-register-login-logout


def mainpage(request):
    return render(request, "mainpage.html")

def login(request):
    if request.method == 'POST':
        staffid = request.POST.get('staffid')
        password = request.POST.get('password')
        User = authenticate(staffid=staffid, password=password)
        if User:
            if User.is_active:
                login(request,User)
                template = loader.get_template("mainpage.html")
                return HttpResponse(template.render())
            else:
                return HttpResponse("Your account is inactive.")
        else:
            print("Your ID or Password is wrong.")
            print("They used username: {PXXXXXXXX} and password: {iicpXXXXXXXXXXXX}".format(staffid,password))
            return HttpResponse("Invalid login details given")
    else:
        form = FormUser(None)
    return render(request, 'login.html', { 'form' : form })
    
    

    '''if request.method == "POST":
        form = User(request, data=request.POST)
        if form.is_valid():
            nm = User.cleaned_data['name']
            em = fm.cleaned_data['email']
            pw = fm.cleaned_data['password']
            reg = User(name=nm, email=em, password=pw)
            reg.save()
            staffid = form.cleaned_data.get('ID')
            password = form.cleaned_data.get('Password')
            #user = {"name": "WanJing"} #authenticate(username=username, password=password)
            User = form.save()
            User.save()
            if user is not None:
               # login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("homepage",name = user)
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")

    return render(request=request, template_name="login.html")'''

# Lau Wan Jing: https://stackoverflow.com/questions/67629441/django-view-returning-post-instead-of-get-request -- as reference of register function
def register(request):
    if request.method == 'POST':
        form = FormUser(request.POST)
        staffid = request.POST.get('staffid')
        name = request.POST.get('name')
        email = request.POST.get('email')
        User = authenticate(staffid=staffid, name=name, email=email)
        if User.isactive():
            user = form.save()
            user.save()
            user = authenticate(staffid=user.staffid, email=user.email)
            login(request, user)
            return redirect('login.html')
    else:
        form = FormUser(None)
    return render(request, 'register.html', { 'form' : form })

def forgotpassword(request):
    if request.method == 'POST':
        form = FormUser(request.POST)
        email = request.POST.get('email')
        User = authenticate(email=email)
        if User.isactive():
            user = form.save()
            user.save()
            user = authenticate(staffid=user.staffid, email=user.email)
            login(request, user)
            return redirect('login.html')
    else:
        form = FormUser(None)
    return render(request, 'forgotpassword.html', { 'form' : form })

