from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

class CustomManager(BaseUserManager):
    def create_user(self, email: str, password: str = None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        if not password:
            raise ValueError('The password field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,  email: str, password: str = None, **extra_fields):
        extra_fields.setdefault('role', CustomUser.SUPER_ADMIN)
        if password is None:
            raise ValueError('Superuser must have a password')
        return self.create_user(email, password, **extra_fields)
    
    def get_by_natural_key(self, email: str):
        return self.get(email=email)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER = 'user'
    ADMIN = 'admin'
    SUPER_ADMIN = 'superadmin'
    MECHANIC = 'mechanic'

    ROLE_CHOICE = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (SUPER_ADMIN, 'superadmin'),
        (MECHANIC, 'mechanic'),
    ]

    user_id = models.AutoField(primary_key=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=20, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.SmallIntegerField(default=1, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    approved = models.SmallIntegerField(default=1, blank=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICE, default=USER)
    profile_image = models.ImageField(upload_to='profile_images/', default=0)
    remember_token = models.CharField(max_length=100, blank=False, editable=False, unique=True)

    objects = CustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_no']

    def __str__(self) -> str:
        return self.email
    
    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
        db_table = 'custom_user'

    # Custom related_name to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name = 'customuser_groups',
        blank = True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name ='customuser_permissions',
        blank = True
    )

    @property
    def is_staff(self) -> bool:
        return self.role in [self.ADMIN, self.SUPER_ADMIN]

    @property
    def is_superuser(self) -> bool:
        return self.role == self.SUPER_ADMIN



class UserCarRecord(models.Model):
    from admin_app.models import CarBrand, CarModel, CarTrim, CarYear
    
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_details')
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name='car_details')
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='cardetails')
    car_year = models.ForeignKey(CarYear, on_delete=models.CASCADE, related_name='car_details')
    car_trim = models.ForeignKey(CarTrim, on_delete=models.CASCADE, related_name='car_details')
    vin_number = models.CharField(max_length=16, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_car_record'



class BookingAndQuote(models.Model):
    from admin_app.models import CarBrand, CarModel, CarTrim, CarYear, ServiceType, ServiceCategory, Services, SubService, SubServiceOption, Location
    
    BOOKING_STATUS = {
        # this content is write according to steps
        
        'Pending for Quote':'pending for quote',
        'Quoted':'quoted',
        'Progressing': 'progressing',
        'Scheduled':'scheduled',
        'Pending':'pending',
        'Deleted':'deleted',
        'Complete':'complete',
        'Cancelled':'cancelled',
    }

    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_service', blank=False, null=True)
    service_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='service_location')
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name='service_car_brand')
    car_year = models.ForeignKey(CarYear, on_delete=models.CASCADE, related_name='service_car_year')
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='service_car_model')
    car_trim = models.ForeignKey(CarTrim, on_delete=models.CASCADE, related_name='service_car_trim')
    car_vno = models.CharField(max_length=16, blank=True, null=True)
    car_service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='car_service_type')
    car_service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='car_service_category')
    car_services = models.CharField(max_length=500)
    status = models.CharField(max_length=50, choices=BOOKING_STATUS, default='pending for quote', blank=True, null=True)
    mechanic = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assign_mechanic', blank=True, null=True)
    total_service_amount = models.FloatField(blank=False, null=True)
    parts_amount = models.FloatField(blank=False, null=True)
    labour_amount = models.FloatField(blank=False, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    schedule_at = models.CharField(blank=True, null=True)
    schedule_time_slot = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'booking'       
        


class SubServiceAndOption(models.Model):
    from admin_app.models import Services
    id = models.AutoField(primary_key=True)
    booking_id = models.ForeignKey(BookingAndQuote, on_delete=models.CASCADE, related_name='booking_id')
    service_id = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='service_id', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sub_service_and_option'

    
class SubServiceBasedOption(models.Model):
    from admin_app.models import SubService
    id = models.AutoField(primary_key=True)
    subServiceAndOptionId = models.ForeignKey(SubServiceAndOption, on_delete=models.CASCADE, related_name='subServiceAndOptionId')
    sub_service = models.ForeignKey(SubService, on_delete=models.CASCADE, related_name='sub_service')
    sub_service_option = models.CharField(max_length=500)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sub_service_based_option'


class MechanicLeaves(models.Model):
    
    id = models.AutoField(primary_key=True)
    mechanic_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mechanic_id')
    start_date = models.DateField()
    end_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mechanic_leaves'



class ServicePayment(models.Model):
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    booking = models.ForeignKey(BookingAndQuote, on_delete=models.CASCADE, related_name='booking')
    service_amount = models.IntegerField()
    status = models.CharField(max_length=200, default='pending') 
    payment_mode = models.CharField(max_length=20, default='cash') 
    stripe_payment_intent_id = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'booking_payment'


    
class UserComboPackage(models.Model):
    from admin_app.models import ComboDetails
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_Id')
    car_id = models.ForeignKey(UserCarRecord, on_delete=models.CASCADE, related_name='car_Id')
    remaining_combo_usage = models.SmallIntegerField(blank=True, null=True, default=0)
    combo = models.ForeignKey(ComboDetails, on_delete=models.CASCADE, related_name='combo_Id')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_combo_package'

    
class UserComboTracking(models.Model):
    from admin_app.models import Services, ServiceType, ServiceCategory, SubService
    
    id = models.AutoField(primary_key=True)
    user_combo_id = models.ForeignKey(UserComboPackage, on_delete=models.CASCADE, related_name='user_combo_id', blank=True, null=True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='combo_service')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='combo_service_type')
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='combo_service_category')
    sub_service = models.CharField(max_length=100, null=True, blank=False)
    sub_service_option = models.CharField(max_length=100, null=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_combo_tracking'
