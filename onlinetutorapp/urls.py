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
    #courselist url
    path('<int:userid>/courselist', views.courselist, name="courselist"),
    path('<int:userid>/coursepage', views.coursepage, name="coursepage"),
    path('<int:userid>/addmaterials', views.addmaterials, name="addmaterials"),
    path('<int:userid>/deletematerials', views.deletematerials, name="deletematerials"),
    #discussionboard url
    path('<int:userid>/deletequestion', views.deletequestion, name="deletequestion"),
    path('<int:userid>/deletecomment', views.deletecomment, name="deletecomment"),
    path('<int:userid>/discussionboard', views.discussionboard, name="discussionboard"),
    path('<int:userid>/search', views.search, name="search"),
    path('<int:userid>/addquestion', views.addquestion, name="addquestion"),
    path('<int:userid>/replyquestion/<int:discussionid>', views.replyquestion, name="replyquestion"),
    path('<int:userid>/discussionquestion/<int:id>', views.discussionquestion, name="discussionquestion"),
    #quizzes url
]