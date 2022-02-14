from unittest import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from .forms import FormHomePage, FormTodolist, FormUser,FormHomePage
from django.contrib import messages
from django.core.mail import send_mail


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

def register_page(request):
    if(request.GET.get('submitbutton')):
        if request.method == 'POST':
            captcha = request.POST.get('registercaptcha')
            if captcha.is_valid():
                request.GET.get('register')
                form = FormUser(request.POST)
                staffid = request.POST.get('staffid')
                name = request.POST.get('name')
                email = request.POST.get('email')
                for i in register_page:
                    password = User.objects.make_random_password()
                    i.set_password(password)
                    i.save(update_fields=['password_hash'])
                U = User(isactive=True)
                U.save
                User = staffid, name, email
                User = form.save()
                User.save()
                return HttpResponseRedirect('login.html')
            else:  
                return HttpResponse('Captcha failed.')
        else:
            form = FormUser(None)
            messages.error(request,'Please try again.')
        return render(request, 'register.html', { 'form' : form })
    else:
        form = FormUser(None)
    return render(request, 'register.html', { 'form' : form })

# Lau Wan Jing: https://stackoverflow.com/questions/67629441/django-view-returning-post-instead-of-get-request -- as reference of register function

    '''def register(request):
    if(request.GET.get('submitbutton')):
        if request.method == 'POST':
            for user in register:
                password = user.objects.make_random_password()
                user.set_password(password)
                user.save(update_fields=['password'])
            form = FormUser(request.POST)
            captcha = request.POST.get('registercaptcha')
            if captcha.is_valid():
                staffid = request.POST.get('staffid')
                name = request.POST.get('name')
                email = request.POST.get('email')
                user = staffid, name, email, password_hash, isactive
                user = form.save()
                user.save()
                return redirect('login.html')
            else:
                messages.error(request, 'Captcha failed')
        else:
            form = FormUser(None)
        return render(request, 'register.html', { 'form' : form })'''



# Lau Wan Jing: https://www.tutorialspoint.com/how-to-add-a-captcha-in-a-django-website -- captcha 

'''def captcha(request):
    if request.method=="POST":
        form = FormCaptcha(request.POST)
        captcha = request.POST.get('registercaptcha')
        if captcha.is_valid():
            print("success")
        else:
            print("fail")
    else:
        form=FormCaptcha()
    return render(request,"register.html",{ 'form' : form })'''


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

def send_mail(request):
    sender_email = "etutor4007@gmail.com"
    
    sender_password = "etutorwjwc"
    
    receiver_email = "lauwan08@gmail.com"
    
    'New question from E-Tutor Helpdesk',
    
    '{user}',
    'etutor4007@gmail.com',
    ['lauwan08@gmail.com'],
    
    fail_silently=False,

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