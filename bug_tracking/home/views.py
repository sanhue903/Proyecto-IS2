from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request,'home/start.html')





