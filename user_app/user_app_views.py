import os
import json
import hashlib
import fastjsonschema
import schemas.login_schema
import schemas.registration_schema

from admin_app.models import *
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from user_app.models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from schemas.login_schema import validate_login
from django.template import TemplateDoesNotExist 
from user_app.forms import CustomUserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache 
from schemas.registration_schema import validate_registration
from django.contrib.auth import authenticate, login as auth_login 
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
# from user_app.user_views import get_caryear_options, get_carmodel_options, get_cartrim_options

curl = settings.CURRENT_URL
media_path = f'{settings.MEDIA_URL}' 

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
    context = {
        'curl': curl
    }
    return render(request, 'home.html', context, status= 200) 

def about(request: HttpRequest) -> HttpResponse:
    """
    This function is used for render the about.html page for.

    Args:
        request 

    Returns:
        HttpResponse: About page of our apllication.
    """
    context = {
        'curl': curl
    }
    return render(request, 'about.html', context, status=200)

def service(request: HttpRequest) -> HttpResponse:
    """
    This function is used for render the service.html page for.

    Args:
        request 

    Returns:
        HttpResponse: service page of our apllication.
    """
    context = {
        'curl': curl
    }
    return render(request, 'service.html', context, status=200)

def team(request: HttpRequest) -> HttpResponse:
    """
    This function is used for render the team.html page for.

    Args:
        request 

    Returns:
        HttpResponse: team list or details of our apllication.
    """
    context = {
        'curl': curl
    }
    return render(request, 'team.html', context, status=200)

def booking(request: HttpRequest) -> HttpResponse:
    """
    This function is used for render the booking.html page for.

    Args:
        request

    Returns:
        HttpResponse: booking page of our apllication.
    """
    context = {
        'curl': curl
    }
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
        if request.method == 'GET':
            form = CustomUserCreationForm()
            referral_token = request.GET.get('referral_token', None)
            print('referral_token',referral_token)

            context = {
                'curl': curl,
                'form': form,
                'referral_token': referral_token,
                }
            
            return render(request, 'register.html', context, status=200)

        elif request.method == 'POST':
            form = CustomUserCreationForm(request.POST, request.FILES)

            file = request.FILES.get('profile_image')
            file_extension = file.name.split('.')[-1].lower() if file else ""

            data = {key: request.POST.get(key) for key in ['email', 'password', 'phone_no', 'last_name', 'first_name']}
            data['profile_image_extension'] = file_extension
            validate_registration(data)

            if CustomUser.objects.filter(email=data.get('email')).exists():
                messages.error(request, "This email is already registered.")
                return redirect('register')
            
            if data.get('password') == request.POST.get('confirm_password'):
                if form.is_valid():

                    user = form.save(commit=False)  
                    image_url = f'{media_path}profile_images/{file.name}' 
                    media_directory = os.path.join(settings.BASE_DIR, 'media/profile_images')
                    user.profile_image = image_url
                    os.makedirs(media_directory, exist_ok=True)

                    file_path = os.path.join(media_directory, file.name)
                    with open(file_path, "wb") as fp:
                        for chunk in file.chunks():
                            fp.write(chunk)

                    user.email = data.get('email').lower()
                    user.set_password(form.cleaned_data['password'])
                    user.remember_token = hashlib.sha256(data.get('email').lower().encode()).hexdigest()

                    referral_token = CustomUser.objects.get(remember_token=request.POST.get('referral_token'))

                    if referral_token:
                        email = UserReferral.objects.get(referred_email=(request.POST.get('email').lower()), referrer_id=referral_token.user_id )
                        email.referred_register_status = True
                        email.save()
                        
                    user.save()
                    messages.success(request, "User register successfully!")
                
                else:
                    email_errors = form.errors
                    messages.error(request, f"{email_errors}")
            else:
                messages.error(request, "Password fields do not match.")
            return redirect('register')
        
        else:
            return redirect('register')
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.registration_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('register')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('register')
    
    except ObjectDoesNotExist:
        messages.error(request, f"Please use the same email address for registration that already used in your referral. Thank you!")
        return redirect('register')
    
    except TemplateDoesNotExist:
        # messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('Home')
    
    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect('register')

def login(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method is used the credential and validate with fastjsonschema and after that login the 
    user and render it according to the user's access like user, admin, super-admin.

    Args:
        request

    Returns:
        HttpResponse: This method is used for login the user admin, super-admin.
    """
    try:
        if request.method == 'GET':
            
            context = {
                'curl':curl
            }
            return render(request, 'login.html', context, status=200)
        
        elif request.method == 'POST':
            
            User = get_user_model()
            data = {
                'email': request.POST.get('email'),
                'password': request.POST.get('password')
            }   
            validate_login(data)

            user = User.objects.get(email=data.get('email'))
            user = authenticate(request, username=data.get('email'), password=data.get('password')) 

            if user is not None:
                if user.status == 1 and user.approved == 1:
                    auth_login(request, user)
                    if user.role == 'user':
                        return redirect('user_dashboard')
                    
                    elif user.role == 'mechanic':
                        return redirect('mechanic_dashboard')
                    
                    else:
                        return redirect('admin_dashboard')
                    
                else:
                    messages.error(request, "Your account is inactive. Please contact to Admin.")
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
    
    except ObjectDoesNotExist:
        messages.error(request, f"No user found with email")
        return redirect('login')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('Home')
    
    except Exception as e :
        messages.error(request, f"{e}")
        return redirect('login')
    

def request_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    # try:
        if request.method == "GET":
            years = CarYear.objects.all().order_by('id').filter(status=1)
            brands = CarBrand.objects.all().order_by('id').filter(status=1)
            locations = Location.objects.all().order_by('id').filter(status=1)

            context = {
                'curl': curl,
                'years': years,
                'brands': brands,
                'locations': locations,
            }
            return render(request, 'service_quote.html', context, status= 200) 
    # except Exception as e:
    #     return redirect('request_data_handler')



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
        
