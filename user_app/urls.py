"""
URL configuration for RevolutionAuto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from user_app import user_app_views, user_views

urlpatterns = [

    # --------------Basic and common urls--------------
    path('', user_app_views.index, name='Home'),
    path('team/', user_app_views.team, name='Team'),
    path('about/', user_app_views.about, name='About'),
    path('login/', user_app_views.login, name='login'),
    path('service/', user_app_views.service, name='Service'),
    path('logout/', user_app_views.logout_view, name='logout'),
    re_path(r'^register/$', user_app_views.register, name='register'),


    # -------------- User urls--------------
    path('user/dashboard', user_views.user_dashboard, name='user_dashboard'),
    path('user/<int:id>/', user_views.user_userapp_action_handler, name='user_userapp_action_handler'),

    
    path('user-cars/', user_views.user_car_data_handler, name='user_car_data_handler'),
    path('user-cars/<int:id>/', user_views.user_car_action_handler, name='user_car_action_handler'),
    path('car-service-history/', user_views.car_service_history, name='car_service_history'),


    # -------------- Add Car detail from options urls--------------
    path('get-caryear-options/', user_views.get_caryear_options, name='get_caryear_options'),
    path('get-cartrim-options/', user_views.get_cartrim_options, name='get_cartrim_options'),
    path('get-carmodel-options/', user_views.get_carmodel_options, name='get_carmodel_options'),


    # -------------- Referral based urls--------------
    path('user-referral/', user_views.referral_data_handler, name='referral_data_handler'),


    # -------------- Notification based urls--------------
    path('user-notification/', user_views.user_notification_data_handler, name='user_notification_data_handler'),
    path('user-notification/<int:id>/', user_views.user_notification_action_handler, name='user_notification_action_handler'),


    # -------------- Service and Bookings based urls--------------
    path('user/request-a-quote', user_app_views.request_data_handler, name='request_data_handler'),


    # -------------- Service and Bookings based urls--------------
    path('get-services/', user_app_views.get_services, name='get_services'),
    path('get-sub-service/', user_app_views.get_sub_service, name='get_sub_service'),
    path('get-service-category/', user_app_views.get_service_category, name='get_service_category'),
    path('get-sub-service-option/', user_app_views.get_sub_service_option, name='get_sub_service_option'),

    path('check-login/', user_app_views.check_login, name='check_login'),
    path('user-booking/', user_views.user_booking_data_handler, name='user_booking_data_handler'),
    path('book-appointment/<int:id>', user_views.book_appointment_handler, name='book_appointment_handler'),
    path('booking-service/<int:id>', user_app_views.booking_service_handler, name='booking_service_handler'),

    path('create_checkout_session/<int:id>', user_views.create_checkout_session, name='create_checkout_session'),
    path('payment/success/', user_views.payment_success, name='payment_success'),
    path('payment/cancel/', user_views.payment_cancel, name='payment_cancel'),
    path('payments/', user_views.user_payment, name='user_payment'),

    path('combos/', user_views.user_combo_data_handler, name='user_combo_data_handler'),
    path('combo/operation/<int:id>', user_views.combo_action_handler, name='combo_action_handler'),
    path('combo/booking/', user_views.user_combo_handler, name='user_combo_handler'),

    path('combo-create-checkout-session/<int:id>', user_views.combo_create_checkout_session, name='combo_create_checkout_session'),
    path('combo-payment-success/', user_views.combo_payment_success, name='combo_payment_success'),
    path('combo-payment-cancel/', user_views.combo_payment_cancel, name='combo_payment_cancel'),

    path('forget-password/', user_app_views.forget_password_handler, name='forget_password_handler'),
    path('reset-password/<str:token>/', user_app_views.reset_password_handler, name='reset_password_handler'),

]
