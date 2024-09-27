import os
import json
import schemas 
import fastjsonschema
import schemas.registration_schema

from django.conf import settings
from django.contrib import messages
from admin_app.utils.utils import *
from .forms import AdminRegisterForm
from user_app.models import CustomUser
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache 
from django.contrib.auth.decorators import login_required
from schemas.registration_schema import validate_registration, validate_update_profile_details_schema
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

curl = settings.CURRENT_URL
admin_curl = f"{curl}/admin/"
media_path = f'{settings.MEDIA_URL}'

    
@never_cache
@login_required
def dashboard(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """This method is use to render the dashboard page for Admin and show other different options.

    Args:
        request

    Returns:
        Httprequest: This method is use for render the Admin dashboard page.
    """
    try:
        if request.method == 'GET':
            page_obj = brand_pagination(request)
            all_users = CustomUser.objects.all().order_by('user_id').filter(role='user').count()
            active_users = CustomUser.objects.all().order_by('user_id').filter(role='user', status='1').count()
            approved_mechanics = CustomUser.objects.all().order_by('user_id').filter(role='mechanic', approved='1').count()
            page_obj = brand_pagination(request)
            page_obj = brand_pagination(request)

            context = {
                'curl':admin_curl,
                'page_obj': page_obj,
                'all_users': all_users,
                'active_users': active_users,
                'approved_mechanics': approved_mechanics,
            }
            return render(request, 'admin_dashboard.html', context)
        else:
            return redirect('admin_dashboard')

    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('admin_registration')
    
    except Exception as e:                
        messages.error(request, f"{e}")        
        return redirect('admin_registration')


def admin_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    try:
        if request.method == 'GET':

            context={
                 'curl': curl,
                 'page_obj': admin_pagination(request)
            }
            return render(request, 'admin/admin_management.html',  context)
        
        elif request.method == 'POST':
            form = AdminRegisterForm(request.POST, request.FILES)

            file = request.FILES.get('profile_image')
            file_extention = file.name.split('.')[-1].lower() if file else ""

            data = {key: request.POST.get(key) for key in ['email', 'password', 'phone_no', 'last_name', 'first_name']}
            unique_email = CustomUser.objects.filter(email=data.get('email')).exists()
            
            if not unique_email:
                data['profile_image_extention'] = file_extention
                validate_registration(data)

                if form.is_valid():
                    admin = form.save(commit=False)
                    image_url = f'{media_path}profile_images/{file.name}' 
                    media_directory = os.path.join(settings.BASE_DIR, 'media/profile_images')
                    admin.profile_image = image_url
                    os.makedirs(media_directory, exist_ok=True)

                    file_path = os.path.join(media_directory, file.name)
                    with open(file_path, "wb") as fp:
                        for chunk in file.chunks():
                            fp.write(chunk)

                    admin.set_password(form.cleaned_data['password'])
                    admin.role = 'admin'

                    admin.save() 

                    messages.success(request, f"You are registerd as a 'Admin'")
                    return redirect('admin_data_handler')
                
            else:
                messages.error(request, "Admin with same email is already register, try again with different email id.")
                return redirect('admin_data_handler')
            
        else:
            context = {
                'form': AdminRegisterForm(), 
                'curl': curl,
            }
            return render(request, 'admin/admin_management.html')
                
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.registration_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('admin_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('admin_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('admin_dashboard')
    
    except Exception as e:                
        messages.error(request, f"{e}")        
        return redirect('admin_data_handler')
    
    except Exception as e:
        print(e)
        return redirect('admin_data_handler')


def admin_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    try:
        if request.method == 'POST':
            admin_object = CustomUser.objects.get(user_id=id)
            
            uploaded_file = request.FILES.get('profile_image')
            data = {key: request.POST.get(key) for key in ['email', 'phone_no', 'last_name', 'first_name']}
            page_redirection = 'admin_dashboard' if request.user.email == data.get('email') else 'admin_data_handler'

            if uploaded_file:
                data['profile_image_extention'] = uploaded_file.name.split('.')[-1].lower()
            validate_update_profile_details_schema(data)

            admin_object.first_name = data.get('first_name', admin_object.first_name)
            admin_object.last_name = data.get('last_name', admin_object.last_name)
            admin_object.phone_no = data.get('phone_no', admin_object.phone_no)
            admin_object.email = data.get('email', admin_object.email)
            admin_object.status = request.POST.get('status', admin_object.status)

            if uploaded_file:
                image_url = f"{media_path}profile_images/{uploaded_file.name}"
                media_directory = os.path.join(settings.BASE_DIR, 'media/profile_images')
                admin_object.profile_image = image_url
                os.makedirs(media_directory, exist_ok=True)

                file_path = os.path.join(media_directory, uploaded_file.name)
                with open (file_path,'wb') as data:
                    for chunks in uploaded_file.chunks():
                        data.write(chunks)

            admin_object.save()
            messages.success(request, "Updated successfully !!")
            return redirect(page_redirection)
        
        elif request.method == 'DELETE':
            admin_object = CustomUser.objects.get(user_id=id)
            
            if admin_object:
                admin_object.delete()

                messages.success(request, "Deleted successfully!")
                return redirect(page_redirection)
        else:
            user_pagination_object = user_pagination(request)

            context = {
                'curl' : admin_curl, 
                'page_obj' : user_pagination_object,
            }
            
            return render(request, 'admin/admin_management.html', context)  
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.update_detail_schema.
                       get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect(page_redirection)
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect(page_redirection)
    
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect(page_redirection)
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')

    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect(page_redirection)
    