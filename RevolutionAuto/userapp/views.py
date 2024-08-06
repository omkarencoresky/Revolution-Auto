from django.conf import settings # type: ignore
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, HttpResponse # type: ignore
from django.contrib.auth import authenticate, login as auth_login # type: ignore

curl = settings.CURRENT_URL

# Create your views here.

def index(request) -> HttpResponse:
    """
    This function is used for render the home.html page for.

    Args:
        request 

    Returns:
        HttpResponse: Home page of our apllication.
    """
    return render(request, 'home.html', {'curl':curl}) 

def about(request) -> HttpResponse:
    """
    This function is used for render the about.html page for.

    Args:
        request 

    Returns:
        HttpResponse: About page of our apllication.
    """
    return render(request, 'about.html')

def service(request) -> HttpResponse:
    """
    This function is used for render the service.html page for.

    Args:
        request 

    Returns:
        HttpResponse: service page of our apllication.
    """
    return render(request, 'service.html')

def team(request) -> HttpResponse:
    """
    This function is used for render the team.html page for.

    Args:
        request 

    Returns:
        HttpResponse: team list or details of our apllication.
    """
    return render(request, 'team.html')

def booking(request) -> HttpResponse:
    """
    This function is used for render the booking.html page for.

    Args:
        request 

    Returns:
        HttpResponse: booking page of our apllication.
    """
    return render(request, 'booking.html')

def login(request) -> HttpResponse:
    """
    This function is used for render the login.html page for.

    Args:
        request 

    Returns:
        HttpResponse: login page of our apllication used for user login.
    """
    return render(request, 'login.html')


def register(request) -> HttpResponse :
    """
    If the request is get than it render the register page or if the request is post it apply the register logic.

    Args:
        request

    Returns:
        HttpResponse: if get request render to the register page if request is post than register the user.
    """

    if request.method == 'GET':
        form = CustomUserCreationForm()
        return render(request, 'register.html')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print("set password")
        if form.is_valid():
            print("User Saved")
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "You are registered successfully")
            return redirect('Home') 
        
    
def user_login(request) -> HttpResponse:
    """
    This method is used the credential and validate with fastjsonschema and after that login the 
    user and render it according to the user's access like user, admin, superadmin.

    Args:
        request

    Returns:
        HttpResponse: This method is used for login the user admin, superadmin.
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, f"No user found with email: {email}")
            return render(request, 'login.html')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                if user.role == 'user':
                    return redirect('user_dashboard')  
                elif user.role == 'admin':
                    return redirect('admin_dashboard')  
                else:
                    return redirect('superuser_dashboard')  
            else:
                messages.error(request, "Account is inactive. Please contact support.")
        else:
            messages.error(request, "Invalid email or password. Please try again.")
        
        return render(request, 'login.html')
    
    return render(request, 'login.html')
 