from django import forms
from onlinetutorapp.models import User

class FormUser(forms.ModelForm):
    class Meta:
        model= User
        fields= ["staffid", "name", "email", "password_hash","isactive"]