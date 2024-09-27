import os 
import json
import fastjsonschema
import schemas.registration_schema
import schemas.login_schema

from django.conf import settings
from django.contrib import messages
from user_app.models import CustomUser
from django.shortcuts import render, redirect
from mechanic_app.forms import AddMechanicForm
from django.template import TemplateDoesNotExist 
from django.views.decorators.cache import never_cache 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from schemas.registration_schema import validate_mechanic_register_detail_schema,validate_mechanic_update_detail_schema


curl = settings.CURRENT_URL
media_path = f'{settings.MEDIA_URL}'

def register_mechanic_application(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This function is used for render the mechanic register page or register a new mechanic.

    Args:
        request: If request method is get than render a register page and if the request is post than add the new mechanic record. 

    Returns:
        HttpResponse: If request method get show mechaninc register page of or if request post add new mechanic.
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
            unique_email = CustomUser.objects.filter(email=data.get('email')).exists()


            if not unique_email:
                data['profile_image_extention'] = file_extention
                validate_mechanic_register_detail_schema(data)
                
                if data.get('password') == request.POST.get('confirm_password'):

                    if form.is_valid():
                        mechanic = form.save(commit=False)

                        image_url = f'{media_path}profile_images/{file.name}' 
                        media_directory = os.path.join(settings.BASE_DIR, 'media/profile_images')
                        mechanic.profile_image = image_url
                        os.makedirs(media_directory, exist_ok=True)

                        file_path = os.path.join(media_directory, file.name)
                        with open(file_path, "wb") as fp:
                            for chunk in file.chunks():
                                fp.write(chunk)

                        mechanic.approved = 0
                        mechanic.role = 'mechanic'
                        mechanic.set_password(form.cleaned_data['password'])
                        mechanic.save()
                        
                        messages.success(request, "Your Details recorded, wait until confirmation.")
                        context = {
                            'curl': curl
                        }
                        return render(request, 'home.html', context)
                    
                    else:
                        messages.error(request, "Invalid input field, try again")
                    
                else:
                    messages.error(request, "Password field not matched, try again later.")
            else:
                messages.error(request, "This email is already register, try again with new mail.")
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
        return render(request, 'home.html')

@never_cache
@login_required
def mechanic_dashboard(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This function is used for render the mechanic dashboard page.

    Args:
        request: If request method is get than render a mechanic dashboard page. 

    Returns:
        HttpResponse: If request method get show mechaninc dashboard page.
    """
    try:
        if request.method == 'GET':
            mechanic = request.user
            context = {
                'curl':curl,
                # 'mechanic':mechanic
            }
            return render(request, 'mechanic_dashboard.html', context)
        
        else:
            return redirect('mechanic_dashboard')
        
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('Home')
    
    except Exception as e:
        return redirect('mechanic_dashboard')


@login_required
def mechanic_mechanicapp_data_controller(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This function is used for perform the mechanic related task like update or delete.

    Args:
        request: If request method is POST than update the current data and if the request is DELETE than delete the mechanic record.
        id: Mechanic id used for update or delete the data of mechanic according to the mechanic id . 

    Returns:
        HttpResponse: If request method post than update the mechanic data or if request method is delete than remove the mechanic data according to the id.
    """

    try:
        if request.method == 'POST':
            mechanic_object = CustomUser.objects.get(user_id=id)
            uploaded_file = request.FILES.get('profile_image')
            data = {key: request.POST.get(key) for key in ['email', 'phone_no', 'last_name', 'first_name']}

            if uploaded_file:
                image_extention = uploaded_file.name.split('.')[-1].lower()
                data['profile_image_extention'] = image_extention
            validate_mechanic_update_detail_schema(data)

            mechanic_object.first_name = data.get('first_name', mechanic_object.first_name)
            mechanic_object.last_name = data.get('last_name', mechanic_object.last_name)
            mechanic_object.phone_no = data.get('phone_no', mechanic_object.phone_no)
            mechanic_object.email = data.get('email', mechanic_object.email)

            if uploaded_file:
                image_url = f"{media_path}profile_images/{uploaded_file.name}"
                media_directory = os.path.join(settings.BASE_DIR, 'media/profile_images')
                mechanic_object.profile_image = image_url
                os.makedirs(media_directory, exist_ok=True)

                file_path = os.path.join(media_directory, uploaded_file.name)
                with open (file_path,'wb') as data:
                    for chunks in uploaded_file.chunks():
                        data.write(chunks)

            mechanic_object.save()
            messages.success(request, "Updated successfully !!")
            return redirect('mechanic_dashboard')
        

        elif request.method == 'DELETE':
            mechanic_object = CustomUser.objects.get(user_id=id)

            if mechanic_object:
                mechanic_object.delete()

                messages.success(request, "Delete successfully !!")
                return redirect('mechanic_dashboard')
            
        else:
            return redirect('mechanic_dashboard')
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.mechanic_update_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('mechanic_dashboard')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('mechanic_dashboard')
    
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect("mechanic_dashboard")
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('Home')

    except Exception as e:
        return redirect('mechanic_dashboard')