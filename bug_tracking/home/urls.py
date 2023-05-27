from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    #path('home', views.home, name='principal'),
    path('', views.home, name='principal'),
    path('login', views.login, name='login'),
    # path('', views.home_inicio, name='principal'),

]
