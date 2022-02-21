from django.urls import path
from onlinetutorapp import views

#URLConfig
urlpatterns = [
    path('login', views.login, name="login"),
    path('', views.mainpage, name="mainpage"),
    path('register', views.register, name="register"),
    path('helpdesk', views.helpdesk, name="helpdesk"),
    path('forgotpassword', views.forgotpassword, name="forgotpassword"),
    path('<int:userid>/settings', views.settings, name="settings"),
    path('todolist', views.todolist, name="todolist"),
    path('edithomepage', views.edithomepage, name="edithomepage"),
    #path('<int:user.id>/mainpage_user', views.mainpage_user, name="mainpage_user"),
    path('<int:userid>/mainpage_user', views.showedithomepagebutton_mainpage_user, name="mainpage_user"),
]