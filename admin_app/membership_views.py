import json
import schemas
import hashlib
import fastjsonschema
import schemas.combo_schema
from datetime import datetime
from django.conf import settings
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from admin_app.models import Notification
from admin_app.forms import AddMembership
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist 
from django.core.exceptions import ObjectDoesNotExist
from admin_app.utils.utils import membership_pagination
from django.contrib.auth.decorators import login_required
from schemas.combo_schema import validate_add_combo_schema
from admin_app.utils.utils import specific_account_notification
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

curl = settings.CURRENT_URL
admin_curl = f"{curl}/admin/"


def membership_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect :
    # try:
        if request.method == 'GET':
            membership = membership_pagination(request)
            unread_notification = Notification.get_unread_count(request.user.user_id)
            notifications = specific_account_notification(request, request.user.user_id)
            
            context = {'curl': curl, 
                'page_obj': membership,
                'notifications' : notifications,
                'unread_notification' : unread_notification,
                }
            return render(request, 'membership/membership_management.html', context)

        elif request.method == 'POST':
            form = AddMembership(request.POST)
            if form.is_valid():
                print('form', form)
                form.save()
                messages.success(request, 'Membership is added')
            context = {'curl': curl}
            return render(request, 'membership/membership_management.html', context)
        
        else:
            context = {'curl': curl}
            return render(request, 'membership/membership_management.html', context)

    # except Exception as e :
    #     messages.error(request, f"Something went wrong, try again")
    #     return redirect('membership_handler')