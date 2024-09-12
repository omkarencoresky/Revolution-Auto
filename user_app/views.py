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
from django.template import TemplateDoesNotExist 
from django.views.decorators.cache import never_cache 
from schemas.registration_schema import validate_registration
from django.contrib.auth import authenticate, login as auth_login 
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

curl = settings.CURRENT_URL

context = {
    'curl': curl
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

def register(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    If the request is get than it render the register page or if the request is post it apply the user register logic.

    Args:
        request

    Returns:
        HttpResponse: if get request render to the register page if request is post than register the user.
    """
    try:
        try:
            if request.user.role in ['admin', 'super_user']:
                redirect_template = 'user_data_handler'
            else:
                redirect_template = 'register'
        except :
            redirect_template = 'register'
            
        if request.method == 'GET':
            form = CustomUserCreationForm()

            context = {
                'curl': curl,
                'form': form
                }
            
            return render(request, 'register.html', context, status=200)

        elif request.method == 'POST':
            form = CustomUserCreationForm(request.POST)

            data = {
                'email': request.POST.get('email'),
                'password': request.POST.get('password'),
                'phone_no': request.POST.get('phone_no'),
                'last_name': request.POST.get('last_name'),
                'first_name': request.POST.get('first_name'),
            }
            validate_registration(data)
            


            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()


                messages.success(request, "User register successfully!")
                return redirect(redirect_template)
            
            else:
                messages.error(request, f" This form has not a valid input")
                return redirect(redirect_template)
            
        else:
            # messages.error(request, "Invalid request method")
            return redirect(redirect_template)
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.registration_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect(redirect_template)
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect(redirect_template)
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')
    
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect(redirect_template)
  
def login(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
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
            
            context = {
                'curl':curl
            }
            return render(request, 'login.html', context, status=200)
        
        elif request.method == 'POST':
            
            email = request.POST.get('email')
            password = request.POST.get('password')

            User = get_user_model()
            data = {
                'email': email,
                'password': password
            }   
            validate_login(data)

            user = User.objects.get(email=email)
            user = authenticate(request, username=email, password=password) 

            if user is not None:
                if user.is_active:
                    auth_login(request, user)

                    if user.role == 'user':
                        return HttpResponse('user_dashboard', status=200)
                    
                    else:
                        return redirect('admin_dashboard')
                    
                else:
                    messages.error(request, "Account is inactive. Please contact Admin or Super Admin.")
                    return redirect('Home')
            else:
                messages.error(request, "Invalid email or password. Please try again.")
                return redirect('login')
        else:
            messages.error(request, "Invalid request method")
            return redirect('login')
                
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.login_schema.login_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('login')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('login')
    
    except User.DoesNotExist:
        messages.error(request, f"No user found with email: {email}")
        return redirect('login')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'home.html')
    
    except Exception as e :
        messages.error(request, "An unexpected error occurred. Please try again.")
        return redirect('login')
    
@never_cache
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
        
