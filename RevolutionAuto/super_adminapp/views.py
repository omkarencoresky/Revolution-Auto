from django.shortcuts import render
from django.conf import settings

curl = settings.CURRENT_URL

# Create your views here.

def index(request):
    return render(request, 'home.html', {'curl':curl}) 


def error(request):
    return render(request, 'error.html')


def about(request):
    return render(request, 'about.html')


def service(request):
    return render(request, 'service.html')


def team(request):
    return render(request, 'team.html')


def booking(request):
    return render(request, 'booking.html')

def register(request):
    return render(request, 'register.html')
