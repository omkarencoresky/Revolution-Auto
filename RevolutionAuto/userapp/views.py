import json
import fastjsonschema
import schemas.login_schema
import schemas.registration_schema

from django.conf import settings
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from schemas.login_schema import validate_login
from django.shortcuts import render, redirect, HttpResponse 
from schemas.registration_schema import validate_registration
from django.contrib.auth import authenticate, login as auth_login 

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
    return render(request, 'home.html', {'curl':curl}, status=200) 

def about(request) -> HttpResponse:
    """
    This function is used for render the about.html page for.

    Args:
        request 

    Returns:
        HttpResponse: About page of our apllication.
    """
    return render(request, 'about.html', {'curl':curl}, status=200)

def service(request) -> HttpResponse:
    """
    This function is used for render the service.html page for.

    Args:
        request 

    Returns:
        HttpResponse: service page of our apllication.
    """
    return render(request, 'service.html', {'curl':curl}, status=200)

def team(request) -> HttpResponse:
    """
    This function is used for render the team.html page for.

    Args:
        request 

    Returns:
        HttpResponse: team list or details of our apllication.
    """
    return render(request, 'team.html', {'curl':curl}, status=200)

def booking(request) -> HttpResponse:
    """
    This function is used for render the booking.html page for.

    Args:
        request 

    Returns:
        HttpResponse: booking page of our apllication.
    """
    return render(request, 'booking.html', {'curl':curl}, status=200)

def register(request) -> HttpResponse :
    """
    If the request is get than it render the register page or if the request is post it apply the register logic.

    Args:
        request

    Returns:
        HttpResponse: if get request render to the register page if request is post than register the user.
    """
    try:
        if request.method == 'GET':
            form = CustomUserCreationForm()
            return render(request, 'register.html', {'curl':curl, 'form':form}, status=200)

        if request.method == 'POST':
            data = {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'email': request.POST.get('email'),
                'password': request.POST.get('password'),
                'phone_no': request.POST.get('phone_no')
            }

            try:
                form = CustomUserCreationForm(request.POST)
                validate_registration(data)

                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    messages.success(request, "You are registered successfully")
                    return redirect('Home')
                
                else:
                    messages.error(request, f" This form has not a valid input")
                return render(request, 'register.html', {'curl':curl, 'form':CustomUserCreationForm()}, status=400)
            
            except fastjsonschema.exceptions.JsonSchemaValueException as e:
                messages.error(request,schemas.registration_schema.registration_schema.
                get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
                return render(request, 'register.html', {'curl':curl, 'form':CustomUserCreationForm()}, status=400)
            
            except json.JSONDecodeError:
                messages.error(request, f"{e}")
                return render(request, 'register.html', {'curl':curl, 'form':CustomUserCreationForm()}, status=400)
            except Exception as e:
                messages.error(request, "Internal error, Please try again")
                return render(request, 'register.html', {'curl':curl, 'form':CustomUserCreationForm()}, status=400)

        messages.error(request, "Invalid request method")
        return render(request, 'register.html', {'curl':curl, 'form':CustomUserCreationForm()}, status=405)
    
    except Exception as e:
        messages.error(request, "An unexpected error occurred. Please try again.")
        return render(request, 'register.html', {'curl':curl, 'form':CustomUserCreationForm()},status=500)
  
def login(request) -> HttpResponse:
    """
    This method is used the credential and validate with fastjsonschema and after that login the 
    user and render it according to the user's access like user, admin, superadmin.

    Args:
        request

    Returns:
        HttpResponse: This method is used for login the user admin, superadmin.
    """
    try:
        if request.method == 'GET':
            return render(request, 'login.html', {'curl':curl}, status=200)
        
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            data = {
                'email': email,
                'password': password
            }

            User = get_user_model()

            try:
                validate_login(data)
                user = User.objects.get(email=email)

                if user is not None:
                    if user.is_active:
                        user = authenticate(request, username=email, password=password) 
                        auth_login(request, user)

                        if user.role == 'user':
                            return HttpResponse('user_dashboard', status=200)
                        
                        elif user.role == 'admin':
                            return HttpResponse('admin_dashboard', status=200) 
                        
                        else:
                            return HttpResponse('superuser_dashboard', status=200)  
                        
                    else:
                        messages.error(request, "Account is inactive. Please contact Admin or Super Admin.")
                        return render(request, 'login.html', status=403)
                else:
                    messages.error(request, "Invalid email or password. Please try again.")
                    return render(request, 'login.html', status=401)
                
            except fastjsonschema.exceptions.JsonSchemaValueException as e:
                messages.error(request,schemas.login_schema.login_schema.
                get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
                return render(request, 'login.html', status=400)
            
            except json.JSONDecodeError:
                messages.error(request, f"{e}")
                return render(request, 'login.html', status=400)
            
            except User.DoesNotExist:
                messages.error(request, f"No user found with email: {email}")
                return render(request, 'login.html', status=404)
            
        messages.error(request, "Invalid request method")
        return render(request, 'login.html', status=405)
    
    except Exception as e :
        messages.error(request, "An unexpected error occurred. Please try again.")
        return render(request, 'login.html', status=500)
        
    