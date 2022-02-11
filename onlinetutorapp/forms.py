from django import forms
from onlinetutorapp.models import Helpdesk, Todolist, User
from captcha.fields import CaptchaField

#Lau Wan Jing: https://www.etutorialspoint.com/index.php/255-how-to-insert-data-in-mysql-database-from-an-html-form-using-django

class FormUser(forms.ModelForm):
    captcha=CaptchaField()
    class Meta:
        model= User
        fields= ["staffid", "name", "email"]
        
class FormHelpdesk(forms.ModelForm):
    class Meta:
        model= Helpdesk
        fields= ["question"]
        
class FormTodolist(forms.ModelForm):
    class Meta:
        model= Todolist
        fields= ["task","timeend","status","isactive"]
        
class FormCaptcha(forms.Form):
   captcha=CaptchaField()