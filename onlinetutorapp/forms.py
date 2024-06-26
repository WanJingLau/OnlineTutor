from django import forms
from onlinetutorapp.models import Helpdesk, Homepage, Quiz, Todolist, User, Coursematerial, Discussion, Discussioncomment
from captcha.fields import CaptchaField

#Lau Wan Jing: https://www.etutorialspoint.com/index.php/255-how-to-insert-data-in-mysql-database-from-an-html-form-using-django

class FormUser(forms.ModelForm):
    # Lau Wan Jing: https://www.tutorialspoint.com/how-to-add-a-captcha-in-a-django-website -- captcha
    captcha=CaptchaField()
    
    class Meta:
        model= User
        fields= ["staffid", "name", "email"]
        # https://stackoverflow.com/questions/38724012/django-crispy-forms-set-label-text-for-multiple-fields
        labels = {
            'staffid': 'Lecturer/Student ID',
            'name': 'Full Name',
            'email': 'Email Address',
        }

class FormUserLogin(forms.ModelForm):
    
    class Meta:
        model= User
        fields= ["staffid", "password"]
        
class FormForgotPassword(forms.ModelForm):
    
    class Meta:
        model= Helpdesk
        fields= ["email"]
        
class FormSettings(forms.ModelForm):
    
    class Meta:
        model= User
        fields= ["password"]

class FormMainPage(forms.ModelForm):
    
    class Meta:
        model= Homepage
        fields= ["title"]
        
class FormHelpdesk(forms.ModelForm):
    
    class Meta:
        model= Helpdesk
        fields= ["email", "question"]

class FormTodolist(forms.ModelForm):
    
    class Meta:
        model= Todolist
        fields= ["task","timeend"]
        
class FormHomePage(forms.ModelForm):
    
    class Meta:
        model= Homepage
        fields= ["title","file1","file2"]

class FormAddMaterial(forms.ModelForm):
    class Meta:
        model= Coursematerial
        fields= ["title","description","file","coursetopic"]

class FormAddQuestion(forms.ModelForm):
    class Meta:
        model= Discussion
        fields= ["question","description"]

class FormReplyQuestion(forms.ModelForm):
    class Meta:
        model= Discussioncomment
        fields= ["comment"]
        
class FormAddQuiz(forms.ModelForm):
    class Meta:
        model= Quiz
        fields= ["question","selection","answer"]

class FormAnswerQuiz(forms.ModelForm):
    class Meta:
        model= Quiz
        fields= ["question","selection","answer"]