import json
import fastjsonschema
import schemas.registration_schema

from django.conf import settings
from django.contrib import messages
from user_app.models import CustomUser
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from schemas.registration_schema import validate_update_profile_details_schema

curl = settings.CURRENT_URL+'/'
context = {
                'curl' : curl
            }

@login_required
def user_dashboard(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles displaying User dashboard page with the GET request type.

        Args:
            request: The incoming HTTP request. If GET, it shows the User dashboard page

        Returns:
            HttpResponse: For GET requests, it returns a response with the User dashboard page. 
            If the request is invalid, it renders to the home page with an error message and redirects to the main page.
    """
    try:
        if request.method == 'GET':
            context = {
                'curl' : curl
            }
            return render(request, 'user/user_dashboard.html', context)
        
        else:
            return render(request, 'home.html', context)
        
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'home.html')

    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect("user_dashboard")
    
@login_required
def user_userapp_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating user details when the request type is POST with an ID, and deleting user profile when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the user profile specified by the ID in the request.
            For DELETE requests, it deletes the user profile specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, it shows an error message and redirects to the main page. 
            For DELETE requests, if the deletion is successful, it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """
    try:
        if request.method == 'POST':
                user_object = CustomUser.objects.get(user_id=id)

                data = {
                    'email': request.POST.get('email',user_object.email),
                    'phone_no': request.POST.get('phone_no', user_object.phone_no),
                    'last_name': request.POST.get('last_name', user_object.last_name), 
                    'first_name': request.POST.get('first_name', user_object.first_name),
                }
                validate_update_profile_details_schema(data)

                user_object.email = data.get('email')
                user_object.phone_no = data.get('phone_no')
                user_object.last_name = data.get('last_name')
                user_object.first_name = data.get('first_name')
                user_object.save()

                messages.success(request, "Updated successfully!")
                return redirect("user_dashboard")
        
        elif request.method == 'DELETE':
            user_object = CustomUser.objects.get(user_id=id)

            if user_object:
                user_object.delete()

                messages.success(request, "Deleted successfully!")
                return redirect( 'user_dashboard')
        
        else:
            return render(request, 'user/user_dashboard.html')
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.update_user_detail_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect("user_dashboard")
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect("user_dashboard")
    
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect("user_dashboard")
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'user_dashboard.html')

    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect("user_dashboard")


def referral_data_handler(request):
    user = request.user
    context = {
        'curl' : curl
    }
    return render(request, 'user/user_referral.html', context)