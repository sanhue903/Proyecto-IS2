from django.urls import include, path
from . import views

app_name = "buglist"
urlpatterns = [
    path('', views.index, name='bug_list'),
    path('bugs/', views.index, name='bug_list_pagination'),
    path('bugs/<str:bug_order>/', views.index, name='bug_list_order'),
    path('reports/', views.index, name='report_list_pagination'),
    path('reports/<str:report_order>/', views.index, name='report_list_order'),
]
