import json
import schemas 
import fastjsonschema
import schemas.registration_schema

from django.conf import settings
from django.contrib import messages
from .forms import AdminRegisterForm
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from admin_app.utils.utils import brand_pagination
from django.http import HttpRequest, HttpResponse
from user_app.models import CustomUser
from django.views.decorators.cache import never_cache 
from django.contrib.auth.decorators import login_required
from schemas.registration_schema import validate_registration

curl = settings.CURRENT_URL
admin_curl = f"{curl}/admin/"

def registration(request: HttpRequest) -> HttpResponse:

    """
        Handles the registration of a new admin user.

        This view handles both GET and POST requests:
        - For GET requests, it renders a registration form for the admin user.
        - For POST requests, it processes the form submission:
            1. Validates the registration data using a custom schema.
            2. Saves the new admin user if the form is valid, setting additional fields (`is_staff` and `role`) programmatically.
            3. Provides feedback through success or error messages based on the outcome of the form validation and processing.

        Args:
            request (HttpRequest): The HTTP request object containing metadata and form data.

        Returns:
            HttpResponse: A rendered HTML page with the registration form or a redirect response upon successful registration.
            
        Raises:
            fastjsonschema.exceptions.JsonSchemaException: If the JSON data does not match the expected schema.
            json.JSONDecodeError: If there is an issue decoding JSON data (though this might not be directly relevant if you're not using JSON decoding here).
    """
    try:
        if request.method == 'GET':

            context = {
                'form': AdminRegisterForm(), 
                'curl': curl,
            }
            return render(request, 'admin_registration.html', context, status=200)
        
        elif request.method == 'POST':

            context = {
                'form': AdminRegisterForm(), 
                'curl': curl,
            }
            form = AdminRegisterForm(request.POST)

            email = request.POST.get('email')
            unique_email = CustomUser.objects.filter(email=email).exists()
            
            if not unique_email:
                data = {
                    'email': email,
                    'password': request.POST.get('password'),
                    'phone_no': request.POST.get('phone_no'),
                    'last_name': request.POST.get('last_name'),
                    'first_name': request.POST.get('first_name'),
                }
                validate_registration(data)

                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.role = 'admin'
                    user.save() 

                    messages.success(request, f"You are registerd as a 'Admin'")
                    return render(request, 'home.html', context, status=200)
                    # return redirect('Home') 
            else:
                messages.error(request, "Admin with same email is already register, try again with different email id.")
                return redirect('admin_registration')
        else:
            context = {
                'form': AdminRegisterForm(), 
                'curl': curl,
            }
            return render(request, 'admin_registration.html', context)
                
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.registration_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('admin_registration')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('admin_registration')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('admin_registration')
    
    except Exception as e:                
        messages.error(request, f"{e}")        
        return redirect('admin_registration')
    
@never_cache
@login_required
def dashboard(request):
    """This method is use to render the dashboard page for Admin and show other different options.

    Args:
        request

    Returns:
        Httprequest: This method is use for render the Admin dashboard page.
    """
    page_obj = brand_pagination(request)

    context = {
        'curl':admin_curl,
        'page_obj': page_obj,
    }
    return render(request, 'admin_dashboard.html', context)
