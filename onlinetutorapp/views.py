from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
# Create your views here.
# request -> response
# request handler / action

def mainpage(request, user):
    return render(request, "mainpage.html", user)

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = {"name": "WanJing"} #authenticate(username=username, password=password)
            if user is not None:
               # login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("homepage",name = user)
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")

    return render(request=request, template_name="login.html")