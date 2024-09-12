import json
import schemas
import fastjsonschema
from django.conf import settings
from django.contrib import messages
import schemas.registration_schema
from user_app.models import CustomUser
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from django.http import HttpResponse, HttpRequest
from admin_app.utils.utils import user_pagination
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from schemas.registration_schema import validate_update_user_detail_schema

curl = settings.CURRENT_URL
admin_curl = f"{curl}/admin/"

@login_required
def user_data_handler(request: HttpRequest):
    try:

        user_pagination_object = user_pagination(request)
        context = {
            'curl' : admin_curl, 
            'page_obj' : user_pagination_object,
        }
        return render(request, 'user/user_management.html', context)
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')

    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect('service_type_data_handler')    
    
@login_required
def user_action_handler(request: HttpRequest, id: int):
    try:
        try:
            if request.user.role in ['admin', 'super_user']:
                redirect_template = 'user_data_handler'
            else:
                redirect_template = 'register'
        except :
            redirect_template = 'register'

        if request.method == 'POST':
            user_object = CustomUser.objects.get(user_id=id)

            data = {
                'email': request.POST.get('email'),
                'phone_no': request.POST.get('phone_no'),
                'last_name': request.POST.get('last_name'),
                'first_name': request.POST.get('first_name'),
            }
            validate_update_user_detail_schema(data)

            user_object.email = data.get('email', user_object.email)
            user_object.phone_no = data.get('phone_no', user_object.phone_no)
            user_object.last_name = data.get('last_name', user_object.last_name)
            user_object.first_name = data.get('first_name', user_object.first_name)
            user_object.status = int(request.POST.get('status'))
            user_object.save()

            messages.success(request, "Updated successfully!")
            return redirect('redirect_template')
        
        elif request.method == 'DELETE':
            user_object = CustomUser.objects.get(user_id=89)
            
            if user_object:
                user_object.delete()

                messages.success(request, "Deleted successfully!")
                return redirect('redirect_template') 

    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.validate_update_user_detail_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect(redirect_template)
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect(redirect_template)
    
    except ObjectDoesNotExist:
        print('ObjectDoesNotExist')
        messages.error(request, f"User does not exist.")
        return redirect(redirect_template)
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')

    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect(redirect_template)