from django.urls import path
from . import views

#URLConfig
urlpatterns = [
    path('mainpage/', views.say_hello)
]