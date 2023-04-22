from django.shortcuts import render
from django.shortcuts import redirect, reverse
from .models import Bug
from database.models import Bug


# Create your views here.

def index(request):
    latest_bug_list = Bug.objects.order_by("id_bug")[:20]
    context = {"latest_bug_list": latest_bug_list}
    return render(request, "buglist/index.html", context)

def buglist_home(request):
    return redirect('home:principal')

def refresh(request):
    return redirect('buglist:index')