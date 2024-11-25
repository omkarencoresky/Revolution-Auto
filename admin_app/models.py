from django.db import models
from django.utils import timezone
from  user_app.models import CustomUser


# Car management Models
class CarBrand(models.Model):

    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=2000, blank=True)
    image_url = models.ImageField(  upload_to='brand_images/')
    status = models.SmallIntegerField(blank=False, default=1)
    remember_token = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table ='car_brand'


class CarYear(models.Model):

    id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=6,blank=False)
    car_id = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    status = models.SmallIntegerField(blank=False, default=1)
    remember_token = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'car_year'


class CarModel(models.Model):

    id = models.AutoField(primary_key=True)
    car_id = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    year_id = models.ForeignKey(CarYear, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=50, blank=False)
    status = models.SmallIntegerField(blank=False,default=1)
    remember_token = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'car_model'


class CarTrim(models.Model):

    id = models.AutoField(primary_key=True)
    car_id = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    year_id = models.ForeignKey(CarYear, on_delete=models.CASCADE)
    model_id = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    car_trim_name = models.CharField(max_length=100, blank=False)
    status = models.SmallIntegerField(blank=False,default=1)
    remember_token = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'car_trim'


# Location Models
class Location(models.Model):

    id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=150, blank=False)
    country_code = models.CharField(max_length=50, blank=False)
    service_availability = models.BooleanField(default=True, blank=False)
    status = models.SmallIntegerField(default=1, blank=False)
    remember_token = models.CharField(max_length=100, blank=True) # Remove it next make migration
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'location'


# Service Models
class ServiceType(models.Model):

    id = models.AutoField(primary_key=True)
    service_type_name = models.CharField(max_length=150, blank=False)
    status = models.SmallIntegerField(default=1, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service_type'


class ServiceCategory(models.Model):

    id = models.AutoField(primary_key=True)
    service_category_name = models.CharField(max_length=150, blank=False)
    service_type = models.ForeignKey(ServiceType,on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service_category'


class Services(models.Model): #Add a column for the popularity of services
    
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    id = models.AutoField(primary_key=True)
    service_title = models.CharField(max_length=150, blank=False)
    description = models.TextField(max_length=5000, blank=True)
    service_category = models.ForeignKey(ServiceCategory,on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1, blank=False)
    is_popular = models.CharField(max_length=5, choices=YES_NO_CHOICES, default='No' ) 
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service'


class SubService(models.Model):
    
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    SELECTION_TYPE_CHOICES = [
        ('Single', 'Single'),
        ('Multiple', 'Multiple'),
    ]

    id = models.AutoField(primary_key=True)
    order = models.SmallIntegerField(blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.SmallIntegerField(default=1, blank=False)
    display_text = models.CharField(max_length=200, blank=True)
    service = models.ForeignKey(Services,on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=False)
    description = models.TextField(max_length=5000, blank=True)
    optional = models.CharField(max_length=5, choices=YES_NO_CHOICES, blank=True) 
    selection_type = models.CharField(max_length=8, choices=SELECTION_TYPE_CHOICES, blank=False ) 

    class Meta:
        db_table = 'sub_service'

    
class Inspection(models.Model):

    id = models.AutoField(primary_key=True)
    inspection_name = models.CharField(max_length=200, blank=False)

    class Meta:
        db_table = 'inspection'


class SubServiceOption(models.Model):
    
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    
    OPTION_TYPE_CHOICES = [
        ('Text Type', 'Text Type'),
        ('Image Type', 'Image Type'),
    ]

    id = models.AutoField(primary_key=True)
    order = models.SmallIntegerField(blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=150, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.SmallIntegerField(default=1, blank=False)
    description = models.TextField(max_length=5000, blank=True)
    recommend_inspection_service = models.ManyToManyField(Inspection, blank=True)
    image_url = models.ImageField(upload_to='media/option_images' ,blank=True, null=True)
    option_type = models.CharField(max_length=20, choices=OPTION_TYPE_CHOICES, blank=False ) 
    sub_service = models.ForeignKey(SubService, on_delete=models.CASCADE, related_name='sub_service_option')
    next_sub_service = models.ForeignKey(SubService, on_delete=models.CASCADE, related_name='next_sub_service_options', blank=True, null=True)

    class Meta:
        db_table = 'sub_service_option'



class Notification(models.Model):

    USER_TYPE_CHOICES = [
        ('user', 'user'),
        ('mechanic', 'mechanic'),
        ('admin', 'admin'),
    ]

    STATUS_CHOICES = [
        ('Sent', 'sent'),
        ('Failed', 'failed'),
    ]

    id = models.AutoField(primary_key=True)
    sender_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender_name')
    recipient_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipient_name', blank= True, null= True)
    recipient_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, blank=False, default=1)
    title = models.CharField(max_length=255)
    email_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank= False, default='complete')
    message = models.TextField(max_length=5000, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification'

    @classmethod
    def get_unread_count(cls, user):
        return cls.objects.filter(recipient_id=user, is_read=False).count()
    
    def mark_as_read(self):
        self.is_read = True
        self.save()


class UserReferral(models.Model):
    REDEEM_STATUS = {
        'Redeemed':'redeemed',
        'Available':'available',
    }

    id=models.AutoField(primary_key=True)
    referrer_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='refer_by')
    referred_email = models.EmailField(max_length=255, blank=False)
    booking_id = models.CharField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    referred_register_status = models.BooleanField(default=False)
    redeem_status = models.CharField(max_length=20, choices=REDEEM_STATUS, blank=False, default='available')

    class Meta:
        db_table = 'user_referral'


    
class ServiceCombo(models.Model):
    
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.CharField(max_length=20, default=0)
    discount_price = models.CharField(max_length=20, default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
