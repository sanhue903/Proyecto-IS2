from django.urls import path, include
from . import views

app_name = "home"
urlpatterns = [
    path('', views.home, name='principal'),
    path('login', views.login, name='login'),
    path('accounts/',include('django.contrib.auth.urls')),

]
