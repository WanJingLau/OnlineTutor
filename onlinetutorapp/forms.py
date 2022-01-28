from django import forms
from onlinetutorapp.models import User

#Lau Wan Jing: https://www.etutorialspoint.com/index.php/255-how-to-insert-data-in-mysql-database-from-an-html-form-using-django

class FormUser(forms.ModelForm):
    class Meta:
        model= User
        fields= ["staffid", "name", "email", "password_hash","isactive"]