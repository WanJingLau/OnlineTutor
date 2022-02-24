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
    #mainpage_user path below
    path('<int:userid>/mainpage_user', views.showedithomepagebutton_mainpage_user, name="mainpage_user"),
    #courselist
    path('<int:userid>/courselist', views.courselist, name="courselist"),
    #coursepage
    path('<int:userid>/coursepage', views.coursepage, name="coursepage"),
    #addmaterials
    path('addmaterials', views.addmaterials, name="addmaterials"),
    #editmaterials
    path('<int:coursematerialid>/editmaterials', views.editmaterials, name="editmaterials"),
    #deletematerials
    path('deletematerials', views.deletematerials, name="deletematerials"),
    #discussionboard
    path('discussionboard', views.discussionboard, name="discussionboard"),
    #discussionquestion
    path('discussionquestion', views.discussionquestion, name="discussionquestion"),
    #addquestion
    path('addquestion', views.addquestion, name="addquestion"),
    #editquestion
    path('editquestion', views.editquestion, name="editquestion"),
    #replyquestion
    path('replyquestion', views.replyquestion, name="replyquestion"),
    #editcomment
    path('editcomment', views.editcomment, name="editcomment"),
]