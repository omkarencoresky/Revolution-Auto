import os
import json
import hashlib
import schemas 
import datetime
import fastjsonschema
import schemas.registration_schema
import schemas.notification_schema

from django.conf import settings
from admin_app.utils.utils import *
from django.contrib import messages
from django.http import JsonResponse
from user_app.models import CustomUser
from django.core.mail import send_mail, send_mass_mail
from admin_app.models import Notification
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from .forms import AdminRegisterForm, AddNotification
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache 
from django.contrib.auth.decorators import login_required
from schemas.notification_schema import validate_notification
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from schemas.registration_schema import validate_registration, validate_update_profile_details_schema

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
            notifications = specific_account_notification(request, request.user.user_id)
            unread_notification = Notification.get_unread_count(request.user.user_id)
            all_users = CustomUser.objects.all().order_by('user_id').filter(role='user').count()
            active_users = CustomUser.objects.all().order_by('user_id').filter(role='user', status='1').count()
            approved_mechanics = CustomUser.objects.all().order_by('user_id').filter(role='mechanic', approved='1').count()

            context = {
                'curl':admin_curl,
                'page_obj': page_obj,
                'all_users': all_users,
                'active_users': active_users,
                'notifications': notifications,
                'approved_mechanics': approved_mechanics,
                'unread_notification': unread_notification,
            }
            return render(request, 'admin/admin_dashboard.html', context)
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
            notifications = specific_account_notification(request, request.user.user_id)
            unread_notification = Notification.get_unread_count(request.user.user_id)

            context={
                 'curl': curl,
                 'page_obj': admin_pagination(request),
                 'notifications': notifications,
                 'unread_notification': unread_notification,
            }
            return render(request, 'admin/admin_management.html',  context)
        
        elif request.method == 'POST':
            form = AdminRegisterForm(request.POST, request.FILES)

            file = request.FILES.get('profile_image')
            file_extension = file.name.split('.')[-1].lower() if file else ""

            data = {key: request.POST.get(key) for key in ['email', 'password', 'phone_no', 'last_name', 'first_name']}
            unique_email = CustomUser.objects.filter(email=data.get('email')).exists()
            
            if not unique_email:
                data['profile_image_extension'] = file_extension
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
                    admin.remember_token = hashlib.sha256(data.get('first_name').encode()).hexdigest()

                    admin.save() 

                    messages.success(request, f"{data.get('first_name')} registered as a 'Admin'")
                    return redirect('admin_data_handler')
                
            else:
                messages.error(request, "Admin with same email is already register, try again with different email id.")
                return redirect('admin_data_handler')
            
        else:
            notifications = specific_account_notification(request, request.user.user_id)
            unread_notification = Notification.get_unread_count(request.user.user_id)

            context = {
                'form': AdminRegisterForm(), 
                'curl': curl,
                'notifications': notifications,
                'unread_notification': unread_notification,
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

            if uploaded_file:
                data['profile_image_extension'] = uploaded_file.name.split('.')[-1].lower()

            validate_update_profile_details_schema(data)

            admin_object.email = data.get('email', admin_object.email)
            admin_object.phone_no = data.get('phone_no', admin_object.phone_no)
            admin_object.last_name = data.get('last_name', admin_object.last_name)
            admin_object.first_name = data.get('first_name', admin_object.first_name)
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
            return redirect('admin_data_handler')
        
        elif request.method == 'DELETE':
            admin_object = CustomUser.objects.get(user_id=id)
            
            if admin_object:
                admin_object.delete()

                messages.success(request, "Deleted successfully!")
                return redirect('admin_data_handler')
        else:
            user_pagination_object = user_pagination(request)
            notifications = specific_account_notification(request, request.user.user_id)
            unread_notification = Notification.get_unread_count(request.user.user_id)

            context = {
                'curl' : admin_curl, 
                'notifications': notifications,
                'page_obj' : user_pagination_object,
                'unread_notification': unread_notification,
            }
            
            return render(request, 'admin/admin_management.html', context)  
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.update_detail_schema.
                       get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('admin_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('admin_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect('admin_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')

    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect('admin_data_handler')
    

def admin_notification_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles show the messages list when the request type is GET and when the request type is POST it allow to send the email/message to the 
        different category based like specific user or mechanic and to send a bulk email/message to the all user or mechanic.

        Args:
            request: The incoming HTTP request. For GET requests, it show all the receive message based on the admin based, 
            and for POST requests, allows to send the mail to users or mechanics.

        Returns:
            HttpResponse: For GET requests it shows the messages list for the specific user based, 
                if the request type is accept the GET it render it on the same page. 
                If the request type is POST it send mail to the user or mechanic's register mail id.
    """
    try:
        if request.method == 'GET':

            current_user = CustomUser.objects.get(user_id=request.user.user_id)
            unread_notification = Notification.get_unread_count(request.user.user_id)
            notifications = specific_account_notification(request, request.user.user_id)

            context = {
                'curl': admin_curl,
                'user': current_user,
                'notifications': notifications,
                'unread_notification': unread_notification,
            }
            return render(request, 'admin/admin_notification.html', context)

        elif request.method == "POST":
            form = AddNotification(request.POST)
            
            sent_to = request.POST.get('sent_to')
            sender_id = request.POST.get('sender_id')
            recipient_type = request.POST.get('recipient_type')

            data = {key:request.POST.get(key) for key in  ['title', 'message', 'recipient_type',]}
            if sent_to == 'specific':
                data['recipient_email'] = request.POST.get('recipient_email')
                
            validate_notification(data)

            if form.is_valid():
                sender_object = CustomUser.objects.get(user_id=sender_id)

                if recipient_type and sent_to == "all":
                    recipient_email_list = all_data(request, recipient_type=recipient_type)

                    mail_content = []
                    for x, recipient in enumerate(recipient_email_list):

                        x =(
                                data.get('title'),
                                data.get('message'),
                                request.user.email,
                                [recipient.email]
                            )
                        mail_content.append(x)
                    send_mass_mail(tuple(mail_content))

                    for recipient in list(recipient_email_list):

                        Notification.objects.create(sender_id=sender_object, 
                                                recipient_id=CustomUser.objects.get(email=recipient.email), recipient_type=recipient_type, 
                                                title= data.get('title'), message=data.get('message'), email_status='Sent', is_read=False
                                                )

                    messages.success(request, f"Message send successfully to all '{recipient_type}' !!")
                    return redirect(admin_notification_data_handler)

                elif recipient_type and sent_to == "specific":
                    specific_recipient = CustomUser.objects.filter(email=data.get('recipient_email')).exists()
                    
                    if specific_recipient:
                        mail = send_mail(data.get('title'), data.get('message'), data.get('sender_id'), [data.get('recipient_email')], fail_silently=False,)
                        # notification.status = 'Sent' if mail else 'Failed'  

                        Notification.objects.create(sender_id=sender_object, 
                                                    recipient_id=CustomUser.objects.get(email=data.get('recipient_email')), 
                                                    recipient_type=recipient_type, title= data.get('title'), 
                                                    message=data.get('message'), email_status='Sent', is_read=False)
                    
                        messages.success(request, f"Message send successfully to '{data.get('recipient_email')}' !!")

                    else:
                        messages.error(request, f"Invalid email entered {data.get('recipient_email')}, try again with other email !!")
                return redirect(admin_notification_data_handler)
                        
            else:
                messages.error(request, f"Invalid input entered, try again")
                return redirect('admin_notification_data_handler')
            
        else:
            current_user = CustomUser.objects.get(user_id=request.user.user_id)
            unread_notification = Notification.get_unread_count(request.user.user_id)
            notifications = specific_account_notification(request, request.user.user_id)

            context = {
                'curl': admin_curl,
                'user': current_user,
                'notifications': notifications,
                'unread_notification': unread_notification,
            }
            return render(request, 'admin/admin_notification.html', context)
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.notification_schema.notification_schema.
                       get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('admin_notification_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('admin_notification_data_handler')
        
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect('admin_notification_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')

    except Exception as e:
        print(e)
        return redirect('admin_notification_data_handler')

def admin_notification_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles update messages status like read or not when user the request type is GET with an ID, and deleting message when the request type is DELETE with an ID.

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
                return redirect('admin_notification_data_handler')
            
        else:
            notifications = specific_account_notification(request, request.user.user_id)
            unread_notification = Notification.get_unread_count(request.user.user_id)

            context = {
                'curl': curl,
                'notifications': notifications,
                'unread_notification': unread_notification,
            }
            return render(request, 'admin_notification.html', context)
        
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect("admin_notification_data_handler")
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('admin_dashboard')

    except Exception as e:
        print(e)
        return redirect('admin_notification_data_handler')