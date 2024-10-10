import os
import json
import fastjsonschema
import schemas.car_schema
import schemas.registration_schema

from admin_app.models import *
from django.conf import settings
from admin_app.utils.utils import *
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from user_app.models import CustomUser, UserCarRecord
from django.views.decorators.cache import never_cache
from django.core.exceptions import ObjectDoesNotExist
from user_app.forms import AddCarRecord, UserReferralForm
from django.contrib.auth.decorators import login_required
from schemas.car_schema import validate_users_car_details
from user_app.utils.utils import User_Car_Record_pagination
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from schemas.registration_schema import validate_update_profile_details_schema

curl = settings.CURRENT_URL+'/'
context = {'curl' : curl}
media_path = f'{settings.MEDIA_URL}'

@never_cache
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
            notifications = specific_account_notification(request, request.user.user_id)
            unread_notification = Notification.get_unread_count(request.user.user_id)
            
            context = {
                'curl' : curl,
                'notifications': notifications,
                'unread_notification': unread_notification,
            }
            return render(request, 'user/user_dashboard.html', context)
        
        else:
            return redirect('Home')
        
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'home.html')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect("user_dashboard")
    
@login_required
def user_userapp_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating user details when the request type is POST with an ID, and deleting user profile when the 
        request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the user profile specified by the ID in the request.
            For DELETE requests, it deletes the user profile specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, 
            it shows an error message and redirects to the main page. For DELETE requests, if the deletion is successful, 
            it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """
    try:
        if request.method == 'POST':
            user_object = CustomUser.objects.get(user_id=id)

            uploaded_file = request.FILES.get('profile_image')
            data = {key: request.POST.get(key) for key in ['email', 'phone_no', 'last_name', 'first_name']}

            if uploaded_file:
                image_extension = uploaded_file.name.split('.')[-1].lower()
                data['profile_image_extension'] = image_extension

            validate_update_profile_details_schema(data)

            user_object.email = data.get('email')
            user_object.phone_no = data.get('phone_no')
            user_object.last_name = data.get('last_name')
            user_object.first_name = data.get('first_name')

            if uploaded_file:
                image_url = f"{media_path}profile_images/{uploaded_file.name}"
                media_directory = os.path.join(settings.BASE_DIR, 'media/profile_images')
                user_object.profile_image = image_url
                os.makedirs(media_directory, exist_ok=True)

                file_path = os.path.join(media_directory, uploaded_file.name)
                with open (file_path,'wb') as data:
                    for chunks in uploaded_file.chunks():
                        data.write(chunks)

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


# @login_required
@require_GET
def get_caryear_options(request):

    car_id = request.GET.get('car_id')
    options = CarYear.objects.filter(car_id=car_id).values('id', 'year')
    return JsonResponse(list(options), safe=False)

# @login_required
@require_GET
def get_carmodel_options(request):
    car_id = request.GET.get('car_id')
    year_id = request.GET.get('year_id')
    options = CarModel.objects.filter(car_id=car_id, year_id=year_id).values('id', 'model_name')
    return JsonResponse(list(options), safe=False)

# @login_required
@require_GET
def get_cartrim_options(request):
    
    car_id = request.GET.get('car_id')
    year_id = request.GET.get('year_id')
    model_id = request.GET.get('model_id')
    options = CarTrim.objects.filter(car_id=car_id, year_id=year_id, model_id=model_id).values('id', 'car_trim_name')

    return JsonResponse(list(options), safe=False)

@login_required
def user_car_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles show the Users car list when the request type is GET and when the request type is POST it allow to save the 
        car for specific user.

        Args:
            request: The incoming HTTP request. For GET requests, it show all the car based on the specific user, 
            and for POST requests, allows to add the car for users.

        Returns:
            HttpResponse: For GET requests it shows the cars list for the specific user based, 
                if the request type is accept the GET it render it on the same page. 
                If the request type is POST it add car for the user.
    """
    try:
        if request.method == 'GET':     
            page_obj = User_Car_Record_pagination(request)
            notifications = specific_account_notification(request, request.user.user_id)
            unread_notification = Notification.get_unread_count(request.user.user_id)

            context = {
                'curl' : curl,
                'page_obj': page_obj,
                'model1_options' : CarBrand.objects.all().values('id','brand'),
                'notifications': notifications,
                'unread_notification': unread_notification,
            }
            return render(request, 'user/user_car.html', context)
        
        elif request.method == 'POST':
            form = AddCarRecord(request.POST)

            vin_num = request.POST.get('vin_number')
            data = {key:request.POST.get(key) for key in ['car_brand', 'car_model', 'car_year', 'car_trim']}

            data['vin_number'] = vin_num if vin_num else ""
            validate_users_car_details(data)  

            unique_record = UserCarRecord.objects.filter(car_brand=data.get('car_brand'),car_model=data.get('car_model'),
                                                         car_year=data.get('car_year'),car_trim=data.get('car_trim'), vin_number=vin_num).exists()
            if not unique_record:
                if form.is_valid():

                    carDetail = form.save(commit=False)
                    carDetail.user_id = request.user
                    carDetail.save()

                    messages.success(request, "Added successful !")
            else:
                messages.error(request, "Similar car details already exist")
            return redirect('user_car_data_handler')

        else:
            page_obj = User_Car_Record_pagination(request)
            notifications = specific_account_notification(request, request.user.user_id)
            unread_notification = Notification.get_unread_count(request.user.user_id)

            context = {
                'curl' : curl,
                'model1_options' : CarBrand.objects.all().values('id','brand'),
                'page_obj': page_obj,
                'notifications': notifications,
                'unread_notification': unread_notification,
            }
            return render(request, 'user/user_car.html', context)
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.car_schema.users_car_detail_schema.
                       get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect("user_car_data_handler")
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect("user_car_data_handler")
    
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect("user_car_data_handler")
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('user_dashboard')

    except Exception as e:
        return redirect('user_car_data_handler')
    

@login_required
def user_car_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating user car details when the request type is POST with an ID, and deleting user car when the request 
        type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the user car specified by the ID in the request.
            For DELETE requests, it deletes the user car specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, 
            it shows an error message and redirects to the main page. For DELETE requests, if the deletion is successful, 
            it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """
    try:
        if request.method == 'POST':

            car_instance = UserCarRecord.objects.get(id=id, )
            form = AddCarRecord(request.POST, instance=car_instance)

            data = {key:request.POST.get(key) for key in ['car_brand', 'car_model', 'car_year', 'car_trim', 'vin_number']}
            validate_users_car_details(data)

            unique_record = UserCarRecord.objects.filter(car_brand=data.get('car_brand'),car_model=data.get('car_model'),
                                                        car_year=data.get('car_year'),car_trim=data.get('car_trim'),
                                                        vin_number=data.get('vin_number')).exists()
            if not unique_record:
                if form.is_valid():

                    form.save()
                    messages.success(request, "Update successfully !")
            else:
                messages.error(request, "Similar car details already exist")
            return redirect('user_car_data_handler')
        
        elif request.method == 'DELETE':
            user_car_instance = UserCarRecord.objects.get(id=id)
            
            if user_car_instance:
                user_car_instance.delete()

                messages.success(request, "Deleted successfully !")
            return redirect("user_car_data_handler")
        
        else:
            return render(request, 'user/user_car.html')
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.car_schema.users_car_detail_schema.
                       get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect("user_car_data_handler")
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect("user_car_data_handler")

    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect("user_car_data_handler")
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'user_dashboard.html')

    except Exception as e:
        return redirect('user_car_data_handler')
    

def user_notification_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles show the messages list when the request type is GET.

        Args:
            request: The incoming HTTP request. For POST requests, it show the readed or unread messages list.

        Returns:
            HttpResponse: For GET requests it shows the messages list for the specific user based. If the request type 
                is accept the GET it render it on the same page.
    """
    try:
        if request.method == "GET":
            notifications = specific_account_notification(request, request.user.user_id)
            unread_notification = Notification.get_unread_count(request.user.user_id)

            context = {
                'curl': curl,
                'notifications': notifications,
                'unread_notification': unread_notification,
            }
            return render(request, 'user/user_notification.html', context)
        
        else:
            notifications = specific_account_notification(request, request.user.user_id)
            unread_notification = Notification.get_unread_count(request.user.user_id)

            context = {
                'curl': curl,
                'notifications': notifications,
                'unread_notification': unread_notification,
            }
            return render(request, 'user/user_notification.html', context)
        
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect("user_notification_data_handler")
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('user_dashboard')

    except Exception as e:
        print(e)
        return redirect('user_notification_data_handler')
    

def user_notification_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles update messages status like read or not when user the request type is GET with an ID, and 
        deleting message when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For GET requests, it updates the message status specified by the ID in the request.
            For DELETE requests, it deletes the message specified by the ID.

        Returns:
            HttpResponse: For GET requests, if the message status is update as read is successful, it redirects to the main page. If the update fails, 
            it shows an error message and redirects to the main page.For DELETE requests, if the deletion is successful, it redirects to the main page. 
            If the deletion fails, it shows an error message and redirects to the main page.
    """
    try:
        if request.method == 'GET':
            notification_object = Notification.objects.get(id=id)
            
            notification_object.is_read = True
            notification_object.save()
            
            notification_read_status= {
                'is_read': notification_object.is_read
            }
            messages.success(request, "This message mark as read")
            return JsonResponse(notification_read_status)

        elif request.method == 'DELETE':
            notification_object = Notification.objects.get(id=id)

            if notification_object:
                notification_object.delete()

                messages.success(request, "Deleted successfully !")
                return redirect('user_notification_data_handler')
            
        else:
            notifications = specific_account_notification(request, request.user.user_id)
            unread_notification = Notification.get_unread_count(request.user.user_id)
            
            context = {
                'curl': curl,
                'notifications': notifications,
                'unread_notification': unread_notification,
            }
            return render(request, 'user/user_notification.html', context)
        
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect("user_notification_data_handler")
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('user_dashboard')

    except Exception as e:
        print(e)
        return redirect('user_notification_data_handler')
    


def referral_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles show the Users referral page for send a referral mail when the request type is GET and when the request type is POST
        it allow to send a mail to the mention email for the referral.

        Args:
            request: The incoming HTTP request. For GET requests, it show the Users referral page for referrals, 
            and for POST requests, allows to send a mail to the mention email for the referral.

        Returns:
            HttpResponse: For GET requests it shows the Users referral page, 
                if the request type is accept the GET it render it on the same page. 
                If the request type is POST it send a mail and render on same page with the successful message.
    """
    try:
        if request.method == 'GET':
            notifications = specific_account_notification(request, request.user.user_id)
            unread_notification = Notification.get_unread_count(request.user.user_id)
                    
            context = {
                'curl' : curl,
                'notifications': notifications,
                'unread_notification': unread_notification,
            }
            return render(request, 'user/user_referral.html', context)
        
        elif request.method == 'POST':
            referred_email = request.POST.get('referred_email').lower()

            already_user = CustomUser.objects.filter(email=referred_email).exists()
            
            if already_user:
                messages.error(request, f"With '{referred_email}' already a user registered")
                return redirect('referral_data_handler')

            instance = UserReferral.objects.get(referred_email=referred_email, referrer_id = request.user.user_id) if (
                UserReferral.objects.filter(referred_email=referred_email, referrer_id = request.user.user_id).exists()) else None
            form = UserReferralForm(request.POST, instance=instance)

            if form.is_valid():
                refer_object = form.save(commit=False )

                user = CustomUser.objects.get(email=request.user.email)
                url = f"http://127.0.0.1:8000/register/{user.remember_token}"

                
                html_content = render_to_string('user/referral_mail.html', {'user': user, 'url': url})
                plain_message = strip_tags(html_content)

                refer_object.referrer_id = user

                send_mail(
                        "Revolution Auto referral !!",
                        plain_message,
                        request.user.email,
                        [referred_email],
                        fail_silently=False,
                )

                refer_object.save()
                messages.success(request, f"Referred successfully send to {referred_email}")
            else:
                messages.error(request, "Please enter at-least one email for referral")
            return redirect('referral_data_handler')
        
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect("referral_data_handler")
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('user_dashboard')

    except Exception as e:
        print(e)
        return redirect('referral_data_handler')
        