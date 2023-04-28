from django.urls import include,path
from . import views


app_name = "buglist"
urlpatterns = [
    path('', views.index, name= 'bug_list'),
    # path('back',views.buglist_home, name='coming_home'),
]