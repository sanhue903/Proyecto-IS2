from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path('home', views.home, name='principal'),
    path('bugs',views.home_buglist,name='buglist'),
    path('confirmacion_reporte', views.confirmacion_reporte, name='confirmacion_reporte'),
    path('reportar_bug', views.reportar_bug, name='reportar_bug'),
]
