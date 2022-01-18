from django.urls import path
from . import views

#URLConfig
urlpatterns = [
    path('', views.login, name="login"),
    path('mainpage/', views.mainpage, name="mainpage"),
]