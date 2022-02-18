import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from onlinetutorapp.models import User
from .forms import FormForgotPassword, FormHomePage, FormTodolist, FormUser,FormHomePage, FormUserLogin
from django.contrib import messages

# Create your views here.
# request -> response
# request handler / action
# Lau Wan Jing: https://itsourcecode.com/free-projects/python-projects/django-login-and-registration-with-source-code/
# Lau Wan Jing: https://ordinarycoders.com/blog/article/django-user-register-login-logout

def mainpage(request):
    return render(request, "mainpage.html")

def mainpage_admin(request):
    return render(request, "mainpage_admin.html")

# Lau Wan Jing: https://www.tutorialspoint.com/how-to-add-a-captcha-in-a-django-website -- captcha 
# Lau Wan Jing: https://www.youtube.com/watch?v=mOS0L5Lb2u0&ab_channel=Desphixs --register function
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
        
# Lau Wan Jing:https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
def sendemail(user):
    subject = 'Welcome to E-Tutor!'
    message = f'Hi {user.staffid}, thank you for registering in E-Tutor web page. Your password is {user.password} and you can sign in into the account now.'
    email_from = "ebook4006@gmail.com"
    recipient_list = [user.email]
    send_mail( subject, message, email_from, recipient_list )

def login(request):
    if request.method == 'POST':
        form = FormUserLogin(request.POST)
        if form.is_valid():
            staffid = form.cleaned_data.get('staffid')
            password = form.cleaned_data.get('password')
            get_login(request, staffid, password)
    else:
        form = FormUserLogin(None)
    return render(request, 'login.html', { 'form' : form })

def get_login(request, staffid, password):
    x = staffid
    y = password
    content = User.objects.raw('SELECT * FROM user WHERE staffid = %s limit 1', [x])
    # Lau Wan Jing: https://stackoverflow.com/questions/1387727/checking-for-empty-queryset-in-django
    if (not(content)):
        messages.error(request, 'Your ID is not found.')
    else:
        for user in content:
            login_verify(request, user, y)
        
def login_verify(request, user, y):
    if user.isactive == 1:
        if user.password == y:
            messages.success(request, f'Welcome {user.staffid}, you are sign in successfully.')
            #cannot work
            redirect_to_mainpage(request)
        else:
            messages.error(request, 'Your password is incorrect. Please try again.')
    else:
        messages.error(request, 'Your account is inactive.')
#cant work
def redirect_to_mainpage(request):
    return render(request, "mainpage.html")

def forgotpassword(request):
    if request.method == 'POST':
        form = FormForgotPassword(request.POST)
        email = request.POST.get('email')
        get_forgotpassword(request, email)
        messages.success(request, 'Please check your email for your password.')
        return redirect('login')
    else:
        form = FormUser(None)
    return render(request, 'forgotpassword.html', { 'form' : form })

def get_forgotpassword(request, email):
    content = User.objects.raw('SELECT * FROM user WHERE email = %s limit 1', [email])
    if (not(content)):
        messages.error(request, 'Your email is not found.')
    else:
        for user in content:
            send_email_forgot_password(user)

def send_email_forgot_password(user):
    subject = 'E-Tutor Online Tutor System'
    message = f'Hi {user.name}, Your password is {user.password} and you can sign in into the account now.'
    email_from = "ebook4006@gmail.com"
    recipient_list = [user.email]
    send_mail( subject, message, email_from, recipient_list )
    
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