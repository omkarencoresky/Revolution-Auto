import os 
import json
import fastjsonschema
import schemas.registration_schema
import schemas.login_schema

from django.conf import settings
from django.contrib import messages
from mechanic_app.models import Mechanic
from django.shortcuts import render, redirect
from mechanic_app.forms import AddMechanicForm
from schemas.login_schema import validate_login
from django.template import TemplateDoesNotExist 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from schemas.registration_schema import validate_mechanic_register_detail_schema


curl = settings.CURRENT_URL
media_path = f'{settings.MEDIA_URL}'

def register_mechanic_application(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This function is used for render the mechanic register page for.

    Args:
        request

    Returns:
        HttpResponse: show mechaninc register page of our apllication.
    """
    try:
        if request.method == 'GET':
            context = {
                'curl': curl
            }
            return render(request, 'mechanic_registration.html', context)
        
        elif request.method == 'POST':
            form = AddMechanicForm(request.POST, request.FILES)
            file = request.FILES.get('profile_image')

            file_extention = file.name.split('.')[-1].lower() if file else ""

            data = {key: request.POST.get(key) for key in ['email', 'password', 'phone_no', 'last_name', 'first_name']}
            data['profile_image_extention'] = file_extention
            validate_mechanic_register_detail_schema(data)

            if data.get('password') == request.POST.get('confirm_password'):
                if form.is_valid():
                    mechanic = form.save(commit=False)

                    image_url = f'{media_path}mechanic_images/{file.name}' 
                    media_directory = os.path.join(settings.BASE_DIR, 'media/mechanic_images')
                    file_path = os.path.join(media_directory, file.name)
                    mechanic.profile_image = image_url
                    os.makedirs(media_directory, exist_ok=True)

                    with open(file_path, "wb") as fp:
                        for chunk in file.chunks():
                            fp.write(chunk)

                    mechanic.set_password(form.cleaned_data['password'])
                    mechanic.save()
                    
                    messages.success(request, "Your Details recorded, wait until confirmation.")
                    return render(request, 'home.html', context)
                
                else:
                    messages.error(request, "Invalid input field, try again")
                    
            else:
                messages.error(request, "Password field not matched, try again later.")
            return redirect('register_mechanic_application')
        
        else:
            context = {
                'curl': curl
            }
            return render(request, 'mechanic_registration.html', context)
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.mechanic_register_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('register_mechanic_application')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('register_mechanic_application')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('Home')
        
    except Exception as e:
        print(e)
        return render(request, 'home.html')


def mechanic_login(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    try:
        if request.method == 'GET':
            
            context = {
                    'curl': curl
                }
            return render(request, 'mechanic_login.html', context)
        
        elif request.method == 'POST':
            data = {
                "email" : request.POST.get('email'),
                "password" : request.POST.get('password')
            }
            validate_login(data)
            mechanic = Mechanic.objects.get(email=data.get('email'))
            if mechanic is not None and check_password(data.get('password'),mechanic.password):
                auth_login(request, mechanic)
                if request.user.is_authenticated and mechanic.approved:
                    messages.success(request, f"Login successfull!!!")
                    return redirect('user_dashboard')
                else:
                    messages.error(request, "You are not approved, please wait till your account approved by Admin.")
            else:
                messages.error(request, "Your password is not correct, try again")
        else:
            return redirect('mechanic_login')
        
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
    
    except Exception as e:
        context = {
                'curl': curl
            }
        return render(request, 'mechanic_login.html', context)