from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path('', views.home, name='principal'),
    path('home', views.home, name='principal'),
    path('', views.home, name='principal'),
]
