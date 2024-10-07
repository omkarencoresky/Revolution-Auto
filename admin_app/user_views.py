import json
import schemas
import hashlib
import fastjsonschema
import schemas.registration_schema

from django.conf import settings
from django.contrib import messages
from user_app.models import CustomUser
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from user_app.forms import CustomUserCreationForm
from admin_app.utils.utils import user_pagination
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout
from schemas.registration_schema import validate_registration, validate_update_profile_details_schema

curl = settings.CURRENT_URL
admin_curl = f"{curl}/admin/"

@login_required
def user_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles displaying user's list when the request type is GET and adding a new user when the request type is POST.

        Args:
            request: The incoming HTTP request. If GET, it shows the user's list. If POST, it processes the logic for adding a new user.

        Returns:
            HttpResponse: For GET requests, it returns a response with the user's list. For POST requests, if the user input is valid, it adds the 
            user and redirects to the main page. If the input is invalid, it renders the form with an error message and redirects to the main page.
    """
    try:
        if request.method == 'GET':
            user_pagination_object = user_pagination(request)

            context = {
                'curl' : admin_curl, 
                'page_obj' : user_pagination_object,
            }
            
            return render(request, 'user/user_management.html', context)
        
        elif request.method == 'POST':

            form = CustomUserCreationForm(request.POST)

            data = {key: request.POST.get(key) for key in ['email', 'password', 'phone_no', 'last_name', 'first_name']}
            validate_registration(data)
            
            if data.get('password') == request.POST.get('confirm_password'):

                if form.is_valid():
                    user = form.save(commit=False)

                    user.set_password(form.cleaned_data['password'])
                    user.remember_token = hashlib.sha256(data.get('first_name').encode()).hexdigest()
                    
                    user.save()
                    messages.success(request, "User register successfully!")
                
                else:
                    email_errors = form.errors.get('email', [])
                    messages.error(request, f"{email_errors}")
            else:
                messages.error(request, "Password fields do not match.")
            return redirect('user_data_handler')
        
        else:
            user_pagination_object = user_pagination(request)

            context = {
                'curl' : admin_curl, 
                'page_obj' : user_pagination_object,
            }
            
            return render(request, 'user/user_management.html', context)          
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.registration_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('user_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('user_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')

    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect('user_data_handler')    
    
@login_required
def user_action_handler(request: HttpRequest, id: int, role=None) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating user item when the request type is POST with an ID, and deleting user item when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the user specified by the ID in the request. For DELETE requests, it deletes the user specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, it shows an error message and redirects to the main page. 
            For DELETE requests, if the deletion is successful, it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """

    try:
        if request.method == 'POST':
            user_object = CustomUser.objects.get(user_id=id)

            data = {
                'email': request.POST.get('email', user_object.email),
                'phone_no': request.POST.get('phone_no', user_object.phone_no),
                'last_name': request.POST.get('last_name', user_object.last_name),
                'first_name': request.POST.get('first_name', user_object.first_name),
            }
            validate_update_profile_details_schema(data)

            user_object.email = data.get('email')
            user_object.role = role if role else 'user'
            user_object.phone_no = data.get('phone_no')
            user_object.last_name = data.get('last_name')
            user_object.first_name = data.get('first_name')
            user_object.status = int(request.POST.get('status',user_object.status))
            user_object.save()

            messages.success(request, "Updated successfully!")
            return redirect('user_data_handler')
        
        elif request.method == 'DELETE':
            user_object = CustomUser.objects.get(user_id=id)
            
            if user_object:
                user_object.delete()

                messages.success(request, "Deleted successfully!")
                return redirect('user_data_handler') 
        else:
            user_pagination_object = user_pagination(request)

            context = {
                'curl' : admin_curl, 
                'page_obj' : user_pagination_object,
            }
            
            return render(request, 'user/user_management.html', context)  
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.update_user_detail_schema.
                       get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('user_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('user_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect('user_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')

    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect('user_data_handler')
    

@login_required
def admin_login_as_user(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles the login with the user's credential when the request type is GET.

        Args:
            request: The incoming HTTP request. If GET, it login with the specific user's credential.

        Returns:
            HttpResponse: For GET requests, it provide the access for the specific user's id and login with the same credetial.
    """
    try:
        if request.method  == 'GET':
            user = CustomUser.objects.get(user_id=id)
            logout(request)
            
            if user is not None:
                auth_login(request, user)

                if request.user.is_authenticated:
                    messages.success(request, f"Login successfull!!!")
                    return redirect('user_dashboard')
                
                messages.error(request, "User is not authenticate")

            else:
                messages.error(request, "User not found, try again")
            return redirect('user_data_handler')
        
        else:
            return redirect('user_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect('user_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')

    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect('user_data_handler')
