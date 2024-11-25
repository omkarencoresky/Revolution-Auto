import os
import json
import stripe
import fastjsonschema
import schemas.car_schema
import schemas.booking_schema
import schemas.registration_schema

from datetime import datetime
from admin_app.models import *
from django.urls import reverse
from django.conf import settings
from django.db import transaction
from admin_app.utils.utils import *
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.decorators.cache import never_cache
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from schemas.car_schema import validate_users_car_details
from user_app.forms import AddCarRecord, UserReferralForm
from user_app.models import CustomUser, UserCarRecord, Service_payment
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from schemas.registration_schema import validate_update_profile_details_schema
from user_app.utils.utils import User_Car_Record_pagination, User_booking_pagination, User_payments_pagination, Combos_pagination


curl = settings.CURRENT_URL+'/'
context = {'curl' : curl}

media_path = f'{settings.MEDIA_URL}'

stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_PUBLISHABLE_KEY = settings.STRIPE_PUBLISHABLE_KEY

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
                'user': request.user,
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
        messages.error(request,schemas.registration_schema.update_detail_schema.
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
    
    try:
        car_id = request.GET.get('car_id')
        options = CarYear.objects.filter(car_id=car_id).values('id', 'year')
        return JsonResponse(list(options), safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error','message': 'Invalid car_id data format'}, status=400)

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'No car found with car_id'}, status=400)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error processing request: {str(e)}'}, status=400)


# @login_required
@require_GET
def get_carmodel_options(request):

    try:
        car_id = request.GET.get('car_id')
        year_id = request.GET.get('year_id')
        options = CarModel.objects.filter(car_id=car_id, year_id=year_id).values('id', 'model_name')
        return JsonResponse(list(options), safe=False)
    
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error','message': 'Invalid car_id data format'}, status=400)

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'No car found with car_id'}, status=400)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error processing request: {str(e)}'}, status=400)


# @login_required
@require_GET
def get_cartrim_options(request):
    try:
        car_id = request.GET.get('car_id')
        year_id = request.GET.get('year_id')
        model_id = request.GET.get('model_id')
        options = CarTrim.objects.filter(car_id=car_id, year_id=year_id, model_id=model_id).values('id', 'car_trim_name')
        return JsonResponse(list(options), safe=False)
    
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error','message': 'Invalid detail data format'}, status=400)

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'No car found with this details'}, status=400)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error processing request: {str(e)}'}, status=400)


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
            page_obj = User_Car_Record_pagination(request, request.user.user_id)
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
    

def car_service_history(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    try:
        car_id = request.GET.get('car_id')
        user_id = request.GET.get('user_id')

        car_details = UserCarRecord.objects.get(id=car_id)
        car_history_list = BookingAndQuote.objects.filter(user=user_id, car_brand=car_details.car_brand, car_year=car_details.car_year, 
                                                            car_model=car_details.car_model, car_trim=car_details.car_trim, 
                                                            total_service_amount__isnull=False).values('service_location', 'car_services', 
                                                            'mechanic', 'total_service_amount', 'created_at', 'schedule_at')
        
        for car_history in car_history_list:
            service_ids = car_history['car_services'].split(',')
            services_title = []

            for service_id in service_ids:
                service_temp = Services.objects.filter(id=service_id).first()
                services_title.append(service_temp.service_title)

            location = Location.objects.filter(id=car_history['service_location']).first()
            mechanic = CustomUser.objects.filter(user_id=car_history['mechanic']).first()

            car_history['service_location'] = location.location_name if location else car_history['service_location']
            car_history['mechanic'] = (mechanic.first_name,' ', mechanic.last_name) if mechanic else car_history['mechanic']
            car_history['car_services'] = services_title if service_ids else car_history['car_services']
        
        return JsonResponse(list(car_history_list), safe=False)
    
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error','message': 'Invalid detail data format'}, status=400)

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'No car found with this details'}, status=400)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error processing request: {str(e)}'}, status=400)


def user_notification_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles show the messages list when the request type is GET.

        Args:
            request: The incoming HTTP request. For POST requests, it show the read or unread messages list.

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
        

def user_booking_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    try:
        if request.method == 'GET':
            bookings = User_booking_pagination(request, request.user.user_id)
            context = {
                'curl': curl,
                'page_obj': bookings,
            }

        else:
            context = {
                'curl': curl,
            }
            messages.error(request, "error")
        return render(request, 'user/user_booking.html',context)
    
    except ObjectDoesNotExist:
        messages.error(request, f"Object does not exist.")
        return redirect('user_booking_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('user_dashboard')

    except Exception as e:
        # print(e)
        return redirect('user_booking_data_handler', e)
    

def book_appointment_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    try:
        if request.method == 'GET':
            
            booking_object = BookingAndQuote.objects.get(id=id) 
            all_object =BookingAndQuote.objects.filter(user=booking_object.user.user_id)

            unavailable_dates = []
            for item in all_object:
                if item.schedule_at != None:
                    unavailable_dates.append( datetime.strptime(item.schedule_at, "%Y-%m-%d"))

            context = {
                'curl': curl,
                'booking_object': booking_object,
                'unavailable_dates': unavailable_dates,
                'selected_loc':booking_object.service_location.location_name,
            }
            
            return render(request, 'user/booking_schedule_calendar.html', context)
        
        elif request.method == 'POST':
            schedule_time_slot = request.POST.get('schedule_time_slot', '')
            schedule_at = request.POST.get('schedule_date', '')
            payment_mode = request.POST.get('payment_mode', '')
            
            booking_object = BookingAndQuote.objects.get(id=id)
            booking_object.schedule_at = schedule_at
            booking_object.schedule_time_slot = schedule_time_slot
            booking_object.status = 'progressing'
            booking_object.save()

            if payment_mode == 'stripe':
                context = {
                    'curl': curl,
                    'booking_object':booking_object,
                    'stripe_public_key': STRIPE_PUBLISHABLE_KEY
                    }
                return render(request, 'booking_payment/checkout.html', context)
            
            elif payment_mode == 'cash':

                Service_payment.objects.create(
                    user=booking_object.user,
                    booking=booking_object,
                    service_amount=booking_object.total_service_amount,
                    payment_mode='cash',
                    status='pending',
                    stripe_payment_intent_id='Not available'
                )
                messages.success(request, f"Your Booking schedule successfully.")
                return redirect('user_payment')

        else:
            messages.error(request, "In-valid request type")
            return redirect('user_booking_data_handler')

    except ObjectDoesNotExist:
        messages.error(request, f"Object does not exist.")
        return redirect('user_booking_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('user_dashboard')

    except Exception as e:
        # print(e)
        return redirect('user_booking_data_handler', e)
    

@csrf_exempt
def create_checkout_session(request, id: int):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        booking_object = BookingAndQuote.objects.select_related('user').get(id=id)
        
        # Get services list
        services = booking_object.car_services.split(',')
        services_object_list = Services.objects.filter(id__in=services).values('service_title')
        services_titles = [service['service_title'] for service in services_object_list]
        services_list = ' | '.join([f" {service} " for i, service in enumerate(services_titles)])

        # Calculate amount in cents and ensure it's positive
        amount = int(float(booking_object.total_service_amount) * 100)
        # if amount <= 0:
        #     raise ValueError("Amount must be greater than 0")

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': amount,
                    'product_data': {
                        'name': f'Booked Services #{booking_object.id}',
                        'description': f"Service and Parts Payment:- {services_list}",
                    },
                },
                'quantity': 1,
            }],
            metadata={
                'booking_id': booking_object.id,
                'user_id': booking_object.user.user_id,
            },
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('payment_success')
            ) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
        )
        return JsonResponse({'success': True, 'checkout_url': checkout_session.url})

    except stripe.error.StripeError as e:
        return JsonResponse({'success': False, 'error': f"Stripe error: {str(e)}"}, status=400)

    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': "Booking not found"}, status=404)
    
    except ValueError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': f"An unexpected error occurred: {str(e)}"}, status=500)


def payment_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "No session ID provided")
        return redirect('user_booking_data_handler')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status != 'paid':
            messages.error(request, "Payment has not been completed")
            return redirect('user_booking_data_handler')

        # Use transaction to ensure database consistency
        with transaction.atomic():
            booking_object = BookingAndQuote.objects.get(id=session.metadata.get('booking_id'))
            
            # Check if payment already recorded
            if not Service_payment.objects.filter(stripe_payment_intent_id=session.payment_intent).exists():
                Service_payment.objects.create(
                    user=booking_object.user,
                    booking=booking_object,
                    service_amount=booking_object.total_service_amount,
                    payment_mode='card',
                    status='succeeded', 
                    stripe_payment_intent_id=session.payment_intent
                )

        context = {
            'session_id': session.id, 'amount_total': session.amount_total / 100,
            'payment_method_types': session.payment_method_types[0],
        }
        
        messages.success(request, 'Payment successful')
        return render(request, 'booking_payment/success.html', context)

    except stripe.error.StripeError as e:
        messages.error(request, f"Stripe error: {str(e)}")

    except ObjectDoesNotExist:
        messages.error(request, "Booking not found")

    except TemplateDoesNotExist:
        messages.error(request, "Template error")

    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
    
    return redirect('user_booking_data_handler')


def payment_cancel(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "No session ID provided")
        return redirect('user_booking_data_handler')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        
        with transaction.atomic():
            booking_object = BookingAndQuote.objects.get(id=session.metadata.get('booking_id'))
            
            # Only create payment record if it doesn't exist
            if not Service_payment.objects.filter(stripe_payment_intent_id=session.payment_intent).exists():
                Service_payment.objects.create(
                    user=booking_object.user,
                    booking=booking_object,
                    service_amount=booking_object.total_service_amount,
                    payment_mode='card',
                    status='failed',
                    stripe_payment_intent_id=session.payment_intent
                )

        context = {
            'session_id': session.id,
            'amount_total': session.amount_total / 100,
            'payment_method_types': session.payment_method_types[0],
        }
        
        messages.warning(request, 'Payment cancelled')
        return render(request, 'booking_payment/failed.html', context)

    except stripe.error.StripeError as e:
        messages.error(request, f"Stripe error: {str(e)}")

    except ObjectDoesNotExist:
        messages.error(request, "Booking not found")

    except TemplateDoesNotExist:
        messages.error(request, "Template error")

    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
    
    return redirect('user_booking_data_handler')


def user_payment(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    try:
        if request.method == 'GET':
            user_payments = User_payments_pagination(request, request.user.user_id)

            context = {
                'curl': curl,
                'page_obj': user_payments
            }
            return render(request, 'user/user_payment.html', context)
        
        else:
            messages.error(request, f"In-valid method, try again.")
            return redirect('user_dashboard')
            
    except ObjectDoesNotExist:
        messages.error(request, f"Object does not exist.")
        return redirect('user_payment')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('user_dashboard')

    except Exception as e:
        # messages.error(request,f'{e}')
        return redirect('user_dashboard')



def user_combo(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    try:
        if request.method == 'GET':
            combos = Combos_pagination(request)

            context = {
                'page_obj': combos,
                'curl': curl,
            }
            return render(request, 'user/combo.html', context)
        
    except Exception as e:
        print(e)
        return redirect('user_dashboard')



# @csrf_exempt
# def stripe_webhook(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
#     print('this is run')
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    
#     endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         return JsonResponse({'error': 'Invalid payload'}, status=400)
    
#     except stripe.error.SignatureVerificationError as e:
#         return JsonResponse({'error': 'Invalid signature'}, status=400)

#     if event['type'] == 'payment_intent.succeeded':
#         print('succeeded is run')
#         payment_intent = event['data']['object']
#         payment_intent_id = payment_intent['id']
        
#         payment = Service_payment.objects.get(stripe_payment_intent_id=payment_intent_id)
#         payment.status = 'succeeded'
#         payment.save()
    
#     elif event['type'] == 'payment_intent.payment_failed':
#         print('failed is run')
#         payment_intent = event['data']['object']
#         payment_intent_id = payment_intent['id']
        
#         payment = Service_payment.objects.get(stripe_payment_intent_id=payment_intent_id)
#         payment.status = 'failed'
#         payment.save()

#     return JsonResponse({'status': 'success'})