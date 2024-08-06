import json
import fastjsonschema
import schemas 
from django.contrib import messages
from django.http import JsonResponse

import schemas.registration_schema
from .forms import AdminRegisterForm
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from schemas.registration_schema import validate_registration

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
    if request.method == 'GET':
        form = AdminRegisterForm()
        return render(request, 'adminregistration.html', {'form': form})
    
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
                messages.success(request, f" This form has not a valid input")
            return render(request, 'adminregistration.html', {'form': form})
        
        except fastjsonschema.exceptions.JsonSchemaValueException as e:
            messages.error(request,schemas.registration_schema.registration_schema.
            get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
            return render(request, 'adminregistration.html', {'form': AdminRegisterForm()})
        
        except json.JSONDecodeError:
            messages.error(request, f"{e}")
            return render(request, 'adminregistration.html', {'form': AdminRegisterForm()})
