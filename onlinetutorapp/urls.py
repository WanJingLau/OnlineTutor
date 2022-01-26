from django.urls import path
from . import views

#URLConfig
urlpatterns = [
    path('login/', views.login, name="login"),
    path('', views.mainpage, name="mainpage"),
]