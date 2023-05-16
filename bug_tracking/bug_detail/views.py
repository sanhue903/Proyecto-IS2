from django.shortcuts import render
from django.shortcuts import redirect

from database.models import Bug

# Create your views here.

def index(request, bug_id):
    bug = Bug.objects.get(id_bug = bug_id)
    context = {"bug": bug}
    return render(request, "bug_detail/index.html", context)