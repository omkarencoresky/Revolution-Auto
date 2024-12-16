from django.conf import settings
import schemas.registration_schema
from django.contrib import messages
from admin_app.models import Notification
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from admin_app.utils.utils import referral_pagination
from django.contrib.auth.decorators import login_required
from admin_app.utils.utils import specific_account_notification
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect


curl = settings.CURRENT_URL
admin_curl = f"{curl}/admin/"

@login_required
def user_referral_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """This method is use to render the referral_management page and show the all referral's list.

    Args:
    -  request: The incoming HTTP request.

    Returns:
    -  Httprequest: This method is use to referral_management and show the all referral's list.
    """
    try:
        if request.method == "GET":
            referral_pagination_object = referral_pagination(request)
            unread_notification = Notification.get_unread_count(request.user.user_id)
            notifications = specific_account_notification(request, request.user.user_id)

            context = {
                'curl' : admin_curl, 
                'notifications' : notifications,
                'page_obj' : referral_pagination_object,
                'unread_notification' : unread_notification,
            }
            return render(request, 'referral/referral_management.html', context)
        else:
            referral_pagination_object = referral_pagination(request)
            unread_notification = Notification.get_unread_count(request.user.user_id)
            notifications = specific_account_notification(request, request.user.user_id)

            context = {
                'curl' : admin_curl, 
                'notifications' : notifications,
                'page_obj' : referral_pagination_object,
                'unread_notification' : unread_notification,
            }
            return render(request, 'referral/referral_management.html', context)
        
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect("user_notification_data_handler")
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('user_dashboard')
    
    except Exception as e:
        return redirect('user_referral_data_handler')