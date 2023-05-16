from django.urls import include,path
from . import views


app_name = "bug_detail"
urlpatterns = [
    path('<int:bug_id>/', views.index, name= 'index'),

]