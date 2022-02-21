from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse
from onlinetutorapp.models import Helpdesk, User, Userrole, Role
from .forms import FormForgotPassword, FormHelpdesk, FormHomePage, FormMainPage, FormTodolist, FormUser,FormHomePage, FormUserLogin
from django.contrib import messages

# Create your views here.
# request -> response
# request handler / action


def mainpage(request):
    return render(request, "mainpage.html")

def mainpage_user(request):
    return render(request, "mainpage_user.html")

def showedithomepagebutton_mainpage_user(request, userid):
    userrole = get_userrole(userid)
    context = {'roleid' : userrole.roleid_id}
    return render(request, 'mainpage_user.html', context)

def get_userrole(userid):
    userid = userid
    content = Userrole.objects.raw('SELECT * FROM userrole WHERE userid = userid limit 1')
    for userrole in content:
        return userrole

# Functions below: REGISTER
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
            insertrole(staffid)
            messages.success(request, f"Hi {fullname}, your account was created successfully! Please check your email for your password.")
            return redirect('login')
    else:
        form = FormUser()
    return render(request, 'register.html', {'form': form})

def get_email_pass(staffid):
    x = staffid
    content = User.objects.raw('SELECT * FROM user WHERE staffid = %s limit 1', [x])
    for user in content:
        sendemail(user)

# Lau Wan Jing: https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
def sendemail(user):
    subject = 'Welcome to E-Tutor!'
    message = f'Hi {user.staffid}, thank you for registering in E-Tutor web page. Your password is {user.password} and you can sign in into the account now.'
    email_from = "ebook4006@gmail.com"
    recipient_list = [user.email]
    send_mail( subject, message, email_from, recipient_list )

# Lau Wan Jing: https://stackoverflow.com/questions/37839867/django-error-cannot-assign-must-be-an-instance
def insertrole(staffid):
    userrole= Userrole.objects.create(userid = User.objects.get(staffid = staffid), roleid = Role.objects.get(name = 'student'))
    userrole.save()

# Functions below: LOGIN
# Lau Wan Jing: https://itsourcecode.com/free-projects/python-projects/django-login-and-registration-with-source-code/
# Lau Wan Jing: https://ordinarycoders.com/blog/article/django-user-register-login-logout
# Lau Wan Jing: https://pythonprogramming.net/user-login-logout-django-tutorial/
def login(request):
    if request.method == 'POST':
        #form = FormUserLogin(request.POST)
        #if form.is_valid():
        staffid = request.POST.get('staffid') #form.cleaned_data.get('staffid')
        password = request.POST.get('password') #form.cleaned_data.get('password')
        if ((staffid == None) or (password == None)):
            messages.error(request, 'Empty Staff ID/Password')
        else:
            user = User.objects.get(staffid = staffid, password =password)
            if (not(user)):
                messages.error(request, 'Incorrect ID/Password. Please try again')
            else:
                if user.isactive == 1:
                    return redirect('mainpage_user', userid = user.id)
                    #return HttpResponseRedirect(reverse('mainpage_user', args=(user.id,)))
    else:
        form = FormUserLogin(None)
    return render(request, 'login.html', { 'form' : form }) #but jump to here

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
            messages.success(request, f'Welcome, you are logged in as {user.staffid}.')
            #userid = user.id
            #mainpage_user(request, userid)this?
            return redirect('mainpage_user')
            #return redirect(request.GET.get('next','/'))
        else:
            messages.error(request, 'Your password is incorrect. Please try again.')
    else:
        messages.error(request, 'Your account is inactive.')

# Functions below: FORGOT PASSWORD
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

# Functions below: HELPDESK
def helpdesk(request):
    if request.method == 'POST':
        form = FormHelpdesk(request.POST)
        email = request.POST.get('email')
        if form.is_valid():
            form.save()
            get_helpdesk_info(email)
            messages.success(request, 'Thanks for you feedback, system owner will contact you via email.')
        else:
            messages.error(request, 'Your information is invalid. Please try again.')
    else:
        form = FormUser(None)
    return render(request, 'helpdesk.html', { 'form' : form })

def get_helpdesk_info(email):
    content = Helpdesk.objects.raw('SELECT * FROM helpdesk WHERE email = %s limit 1', [email])
    for user in content:
        send_email_helpdesk(user)

def send_email_helpdesk(user):
    subject = 'E-Tutor Online Tutor System'
    message = f'Hi system owner, there is a question from E-Tutor system. From {user.email} and the question is {user.question}'
    email_from = "ebook4006@gmail.com"
    # Lau Wan Jing: https://stackoverflow.com/a/48107308 -- error 'to' argument solved
    send_mail(subject, message, email_from, ["lauwan08@gmail.com"])

# functions below: SETTINGS
# userid need to get from mainpage_user()
def settings(request, userid):
    if request.method == 'POST':
        # form = FormUser(request.POST)
        currentpassword = request.POST.get('oldpass')
        newpassword = request.POST.get('newpass')
        confirmnewpassword = request.POST.get('connewpass')
        info = (currentpassword, newpassword, confirmnewpassword)
        if info.is_valid():
            correctpassword_or_not = password_verify(userid, currentpassword)
            if correctpassword_or_not == "yes":
                if newpassword == confirmnewpassword:
                    #Lau Wan Jing: https://djangobook.com/django-tutorials/mastering-django-models/
                    User.objects.filter(id=userid).update(password=newpassword)
                    messages.success(request, 'Your password is changed successfully, please login with new password next time.')
                else:
                    messages.error(request, 'Your new password and confirm new password are incorrect. Please try again.')
            else:
                messages.error(request, 'Your password is incorrect. Please try again.')
        else:
            messages.error(request, 'Your password is invalid. Please try again.')
    else:
        return render(request, 'settings.html')

def password_verify(userid, currentpassword):
    content = User.objects.raw('SELECT * FROM user WHERE id = %s limit 1', [userid])
    for user in content:
        if currentpassword == user.password:
            return str("yes")
        else:
            return str("no")

















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