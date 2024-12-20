import os
import json
import hashlib
import schemas
import fastjsonschema
from django.conf import settings
import schemas.registration_schema
from django.contrib import messages
from user_app.models import CustomUser
from admin_app.models import Notification
from django.shortcuts import render, redirect
from mechanic_app.forms import AddMechanicForm
from django.template import TemplateDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from mechanic_app.utils.utils import mechanic_pagination
from django.contrib.auth.decorators import login_required
from admin_app.utils.utils import specific_account_notification
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from schemas.registration_schema import validate_mechanic_register_detail_schema, validate_mechanic_update_detail_schema

curl = settings.CURRENT_URL
admincurl = f"{curl}/admin/"
media_path = f'{settings.MEDIA_URL}' 

@login_required
def mechanic_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:

    """
    This method handles displaying mechanic list when the request type is GET and adding a new mechanic when the request type is POST.

        Args:
            request: The incoming HTTP request. If GET, it shows the mechanic list. If POST, it processes the logic for adding a new mechanic.

        Returns:
            HttpResponse: For GET requests, it returns a response with the mechanic list. For POST requests, if the user input is valid, it adds the 
            mechanic and redirects to the main page. If the input is invalid, it renders the form with an error message and redirects to the main page.
    """

    try:
        if request.method == 'GET':
            page_obj = mechanic_pagination(request)
            unread_notification = Notification.get_unread_count(request.user.user_id)
            notifications = specific_account_notification(request, request.user.user_id)

            context = {
                'curl' : admincurl,
                'page_obj' : page_obj,
                'notifications' : notifications,
                'unread_notification' : unread_notification
            }

            return render(request, 'mechanic/mechanic_management.html', context)
        
        elif request.method == 'POST':
            form = AddMechanicForm(request.POST, request.FILES)

            file = request.FILES.get('profile_image')
            image_extension = file.name.split('.')[-1].lower() if file else ""

            data = {key: request.POST.get(key) for key in ['email', 'password', 'phone_no', 'last_name', 'first_name']}
            data["profile_image_extension"] = image_extension
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
                    mechanic.role = 'mechanic'
                    mechanic.remember_token = hashlib.sha256(data.get('first_name').encode()).hexdigest()
                    mechanic.save()
                    
                    messages.success(request, "Your Details recorded, wait until confirmation.")
                
                else:
                    messages.error(request, "Invalid input field, try again")
                return redirect('mechanic_data_handler')
                    
            else:
                messages.error(request, "Password field not matched, try again later.")
            return redirect('mechanic_data_handler')
                
        else:
            page_obj = mechanic_pagination(request)
            unread_notification = Notification.get_unread_count(request.user.user_id)
            notifications = specific_account_notification(request, request.user.user_id)

            context = {
                'curl' : admincurl,
                'page_obj' : page_obj,
                'notifications' : notifications,
                'unread_notification' : unread_notification
            }
            return render(request, 'mechanic/mechanic_management.html', context)
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.mechanic_register_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('mechanic_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('mechanic_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('Home')

    except Exception as e:
        return redirect('mechanic_data_handler')
    
@login_required
def mechanic_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    
    """
    This method handles updating mechanic when the request type is POST with an ID, and deleting mechanic when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the mechanic specified by the ID in the request. For DELETE requests, it deletes the item specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, it shows an error message and redirects to the main page. 
            For DELETE requests, if the deletion is successful, it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """

    try:
        if request.method == 'POST':
            mechanic_object = CustomUser.objects.get(user_id=id)

            data = {key: request.POST.get(key) for key in ['email', 'phone_no', 'last_name', 'first_name']}
            file = request.FILES.get('profile_image')

            if file:
                image_extension = file.name.split('.')[-1].lower()
                data['profile_image_extension'] = image_extension

            validate_mechanic_update_detail_schema(data)

            mechanic_object.first_name = data.get('first_name', mechanic_object.first_name)
            mechanic_object.last_name = data.get('last_name', mechanic_object.last_name)
            mechanic_object.phone_no = data.get('phone_no', mechanic_object.phone_no)
            mechanic_object.email = data.get('email', mechanic_object.email)
            mechanic_object.status = int(request.POST.get('status', mechanic_object.status))
            mechanic_object.approved = int(request.POST.get('approved', mechanic_object.approved))

            if file:
                media_directory = os.path.join(settings.BASE_DIR, 'media/mechanic_images/')
                file_path = os.path.join(media_directory, file.name)
                os.makedirs(media_directory, exist_ok=True)

                with open(file_path, 'wb') as fp:
                    for chunks in file.chunks():
                        fp.write(chunks)

                mechanic_object.profile_image = f"{media_path}/mechanic_images/{file.name}"
            mechanic_object.save()

            messages.success(request, "Updated successfully!")
            return redirect('mechanic_data_handler')
        
        elif request.method == 'DELETE':
            mechanic_object = CustomUser.objects.get(user_id=id)

            if mechanic_object:
                mechanic_object.delete()

                messages.success(request, "Deleted successfully!")
                return redirect('mechanic_data_handler')
        else:
            return redirect('mechanic_data_handler')
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.mechanic_update_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('mechanic_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('mechanic_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(request, "Mechanic not found.")
        return redirect('mechanic_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('admin_dashboard')
    
    except Exception as e:
        return redirect('mechanic_data_handler')