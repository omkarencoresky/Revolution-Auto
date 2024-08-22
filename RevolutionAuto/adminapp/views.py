import json
import schemas 
import fastjsonschema
import schemas.registration_schema

from django.conf import settings
from django.contrib import messages
from .forms import AdminRegisterForm
from django.shortcuts import render, redirect
from adminapp.utils.utils import brand_pagination
from django.http import HttpRequest, HttpResponse
from schemas.registration_schema import validate_registration

curl = settings.CURRENT_URL
admincurl = f"{curl}/adminapp/"

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
            form = AdminRegisterForm()
            return render(request, 'admin_registration.html', {'form': form, 'curl': curl}, status=200)
        if request.method == 'POST':
            data = {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'email': request.POST.get('email'),
                'password': request.POST.get('password'),
                'phone_no': request.POST.get('phone_no')
            }
            try:
                form = AdminRegisterForm(request.POST)
                validate_registration(data)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.is_staff = True
                    user.role = 'admin'
                    user.save()
                    messages.success(request, f"{user.first_name} successfully registerd as a Admin!")
                    return redirect('Home') 
                else:
                    messages.error(request, f" This form has not a valid input")
                return render(request, 'admin_registration.html', {'form': AdminRegisterForm()}, status=400) 
            except fastjsonschema.exceptions.JsonSchemaValueException as e:
                messages.error(request,schemas.registration_schema.registration_schema.
                get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
                return render(request, 'admin_registration.html', {'form': AdminRegisterForm()}, status=400)
            except json.JSONDecodeError:
                messages.error(request, f"{e}")
                return render(request, 'admin_registration.html', {'form': AdminRegisterForm()}, status=400)
            except:
                messages.error(request, "Internal error, Please try again")
        messages.error(request, "Invalid request method")        
        return render(request, 'admin_registration.html', {'form': AdminRegisterForm()}, status=405)
    except:
        messages.error(request, "An unexpected error occurred. Please try again.")
        return render(request, 'admin_registration.html', {'form': AdminRegisterForm()}, status=500)
    

def dashboard(request):
    """This method is use to render the dashboard page for Admin and show other different options.

    Args:
        request

    Returns:
        Httprequest: This method is use for render the Admin dashboard page.
    """
    page_obj = brand_pagination(request)

    context = {
        'page_obj': page_obj,
        'curl':admincurl
    }
    return render(request, 'admin_dashboard.html', context)
