from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from onlinetutorapp.forms import FormUser
from django.contrib import messages

# Lau Wan Jing: https://stackoverflow.com/questions/9480641/django-password-generator
def register(request):
    if request.method == 'POST':
        captcha = request.POST.get('registercaptcha')
        if captcha.is_valid():
            form = FormUser(request.POST)
            staffid = request.POST.get('staffid')
            name = request.POST.get('name')
            email = request.POST.get('email')
            for i in register:
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