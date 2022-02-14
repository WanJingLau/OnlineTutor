from django.urls import path
from onlinetutorapp import views

#URLConfig
urlpatterns = [
    path('login', views.login, name="login"),
    path('', views.mainpage, name="mainpage"),
    path('register', views.register_page, name="register"),
    path('helpdesk', views.helpdesk, name="helpdesk"),
    path('forgotpassword', views.forgotpassword, name="forgotpassword"),
    path('settings', views.settings, name="settings"),
    path('todolist', views.todolist, name="todolist"),
    path('edithomepage', views.edithomepage, name="edithomepage"),
]