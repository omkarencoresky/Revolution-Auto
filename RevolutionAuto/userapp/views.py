from django.conf import settings # type: ignore
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, HttpResponse # type: ignore
from django.contrib.auth import authenticate, login # type: ignore

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

def login(request):
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print("set password")
        if form.is_valid():
            print("User Saved")
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('Home') 
    else:
        form = CustomUserCreationForm()
        return render(request, 'register.html')
    


def login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        print('pre')
        user = authenticate(request, username=username, password=password)
        print('pre')
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponse('user_dashboard')
    return render(request, 'login.html')    