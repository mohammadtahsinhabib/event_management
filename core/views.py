from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, "home.html")


@login_required
def no_permission(request):
    return render(request, "no_permission.html")
