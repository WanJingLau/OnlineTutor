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
    path('<int:userid>/todolist', views.todolist, name="todolist"),
    path('edithomepage', views.edithomepage, name="edithomepage"),
    path('<int:userid>/mainpage_user', views.showedithomepagebutton_mainpage_user, name="mainpage_user"),
    path('<int:userid>/courselist', views.courselist, name="courselist"),
    path('<int:userid>/coursepage', views.coursepage, name="coursepage"),
    path('<int:userid>/addmaterials', views.addmaterials, name="addmaterials"),
    path('<int:userid>/deletematerials', views.deletematerials, name="deletematerials"),
    path('<int:userid>/discussionboard', views.discussionboard, name="discussionboard"),
    path('<int:questionid>/<int:userid>/discussionquestion', views.discussionquestion, name="discussionquestion"),
    path('<int:userid>/addquestion', views.addquestion, name="addquestion"),
    path('<int:userid>/replyquestion', views.replyquestion, name="replyquestion"),
    path('addquiz', views.addquiz, name="addquiz"),
]