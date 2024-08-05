import json
import fastjsonschema
from django.http import JsonResponse
from .forms import AdminRegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from error_handlers import get_friendly_error_message
from schemas.registration_schema import validate_registration

def registration(request):
    if request.method == 'POST':
        data = {
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'phone_no': request.POST.get('phone_no'),
            'role': request.POST.get('role')
        }
        try:
            validate_registration(data)

            form = AdminRegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()

                login(request, user)
                return redirect('Home') 
            return render(request, 'adminregistration.html', {'form': form})
        
        except fastjsonschema.exceptions.JsonSchemaException as e:
            friendly_error = get_friendly_error_message(str(e))
            return render(request, 'adminregistration.html', {'form': AdminRegisterForm(), 'error': friendly_error})
        
        except json.JSONDecodeError:
            return render(request, 'adminregistration.html', {'form': AdminRegisterForm(), 'error': 'Invalid JSON'})
        
    else:
        form = AdminRegisterForm()
        return render(request, 'adminregistration.html', {'form': form})