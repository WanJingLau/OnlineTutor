from django.conf import settings
from django.core.mail import send_mail

from unittest import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate

from onlinetutorapp.models import User
from .forms import FormHomePage, FormTodolist, FormUser,FormHomePage
from django.contrib import messages


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

# Lau Wan Jing: https://www.tutorialspoint.com/how-to-add-a-captcha-in-a-django-website -- captcha 
    
def register(request):
    if request.method == "POST":
        form = FormUser(request.POST)
        if form.is_valid():
            form.save()
            fullname = form.cleaned_data.get('name')
            staffid = form.cleaned_data.get('staffid')
            get_email_pass(staffid)
            messages.success(request, f'Hi {fullname}, your account was created successfully! Please check your email for your password.')
            return redirect('login')
    else:
        form = FormUser()
    return render(request, 'register.html', {'form': form})

def get_email_pass(staffid):
    x = staffid
    content = User.objects.raw('SELECT * FROM user WHERE staffid = %s limit 1', [x])
    for user in content:
        sendemail(user)

def sendemail(user):
    subject = 'Welcome to E-Tutor!'
    message = f'Hi {user.staffid}, thank you for registering in E-Tutor web page. Your password is {user.password} and you can sign in into the account now.'
    email_from = "ebook4006@gmail.com"
    recipient_list = [user.email]
    send_mail( subject, message, email_from, recipient_list )

def forgotpassword(request):
    if request.method == 'POST':
        form = FormUser(request.POST)
        email = request.POST.get('email')
        User = authenticate(email=email)
        if User(isactive=True):
            user = form.save()
            user.save()
            user = authenticate(staffid=user.staffid, email=user.email)
            login(request, user)
            return redirect('login.html')
    else:
        form = FormUser(None)
    return render(request, 'forgotpassword.html', { 'form' : form })

def helpdesk(request):
    if request.method == 'POST':
        form = FormUser(request.POST)
        question = request.POST.get('question')
        question.save()
        return redirect('homepage.html')
    else:
        form = FormUser(None)
    return render(request, 'helpdesk.html', { 'form' : form })

def settings(request):
    if request.method == 'POST':
        form = FormUser(request.POST)
        password_hash = request.POST.get('password_hash')
        User = authenticate()
        if User.isactive():
            user = form.save()
            user.save()
            user = authenticate(password_hash=password_hash)
            login(request, user)
            return redirect('homepage.html')
    else:
        form = FormUser(None)
    return render(request, 'settings.html', { 'form' : form })

def todolist(request):
    if request.method == 'POST':
        form = FormTodolist(request.POST)
        task = request.POST.get('task')
        timeend = request.POST.get('timeend')
        status = request.POST('status')
        add = todolist(task=task,timeend=timeend,status=status)
        add.save()
        return render(request,"todolist.html",{'add':add})
    else:
        form = FormTodolist(None)
    return render(request, 'todolist.html', { 'form' : form })

def deletetask(id):
    New = todolist.objects.get(id=id)
    New.delete()
    return redirect('/todolist')

def edithomepage(request):
    if request.method == 'POST':
        form = FormHomePage(request.POST)
        title = request.POST.get('title')
        file1 = request.POST.get('file1')
        file2 = request.POST('file2')
        edit = title,file1,file2
        edit.save()
        return render(request,"edithomepage.html")
    else:
        form = FormHomePage(None)
    return render(request, 'edithomepage.html', { 'form' : form })