from django.urls import path, include
from . import views

app_name = "home"
urlpatterns = [
    path('', views.home, name='principal'),
    path('login', views.login, name='login'),
    
    path('exit', views.exit, name='exit'),
    path('signup', views.signup, name='signup'),
    path('check-username-availability/', views.check_username_availability, name='check_username_availability'),
    path('check-email-availability/', views.check_email_availability, name='check_email_availability'),

]
