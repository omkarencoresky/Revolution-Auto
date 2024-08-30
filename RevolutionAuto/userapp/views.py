import json
import fastjsonschema
import schemas.login_schema
import schemas.registration_schema

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from schemas.login_schema import validate_login
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from schemas.registration_schema import validate_registration
from django.contrib.auth import authenticate, login as auth_login 

curl = settings.CURRENT_URL

context = {
    'curl':curl
}

# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    """
    This function is used for render the home.html page for.

    Args:
        request 

    Returns:
        HttpResponse: Home page of our apllication.
    """
    return render(request, 'home.html', context, status= 200) 

def about(request: HttpRequest) -> HttpResponse:
    """
    This function is used for render the about.html page for.

    Args:
        request 

    Returns:
        HttpResponse: About page of our apllication.
    """
    return render(request, 'about.html', context, status=200)

def service(request: HttpRequest) -> HttpResponse:
    """
    This function is used for render the service.html page for.

    Args:
        request 

    Returns:
        HttpResponse: service page of our apllication.
    """
    return render(request, 'service.html', context, status=200)

def team(request: HttpRequest) -> HttpResponse:
    """
    This function is used for render the team.html page for.

    Args:
        request 

    Returns:
        HttpResponse: team list or details of our apllication.
    """
    return render(request, 'team.html', context, status=200)

def booking(request: HttpRequest) -> HttpResponse:
    """
    This function is used for render the booking.html page for.

    Args:
        request

    Returns:
        HttpResponse: booking page of our apllication.
    """
    return render(request, 'booking.html', context, status=200)

def register(request: HttpRequest) -> HttpResponse:
    """
    If the request is get than it render the register page or if the request is post it apply the user register logic.

    Args:
        request

    Returns:
        HttpResponse: if get request render to the register page if request is post than register the user.
    """
    try:
        if request.method == 'GET':
            form = CustomUserCreationForm()
            context = {
                'curl':curl,
                'form':form
                }
            return render(request, 'register.html', context, status=200)

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
                context = {
                    'curl':curl,
                    'form':form
                    }
                validate_registration(data)

                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    messages.success(request, "You are registered successfully")
                    return redirect('Home')
                
                else:
                    messages.error(request, f" This form has not a valid input")
                return render(request, 'register.html', context, status=400)
            
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
  
def login(request: HttpRequest) -> HttpResponse:
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
            return render(request, 'login.html', context, status=200)
        
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            User = get_user_model()
            data = {
                'email': email,
                'password': password
            }   

            try:
                validate_login(data)
                user = User.objects.get(email=email)

                user = authenticate(request, username=email, password=password) 
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)

                        if user.role == 'user':
                            return HttpResponse('user_dashboard', status=200)
                        
                        elif user.role == 'admin':
                            # return HttpResponse('admin_dashboard', status=200) 
                            return redirect ('admin_dashboard')
                        
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
    
def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    """
    This method is used the logout of user, admin, superadmin with the help of djnago authentication.

    Args:
        request

    Returns:
        HttpResponse: This method is used for logout the user admin, superadmin.
    """
    logout(request)
    messages.success(request, f"logout successfully")
    return redirect('Home')
        
