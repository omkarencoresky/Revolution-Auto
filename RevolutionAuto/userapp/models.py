from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

class CustomManager(BaseUserManager):
    """
    This class is used for manage the user or admin login according to there access.
    """
    def create_user(self, email, password=None, **extra_fields) -> AbstractBaseUser:
        """
        This create_user function is used for the create the user.

        Args:
            email (email): Email for the user login.
            password (text, optional): password for the user login. Defaults to None.

        Returns:
            User    
        """
        if not email:
            raise ValueError('The email field must be set')
        
        if not password:
            raise ValueError('The password field must be set')
            
        email = self.normalize_email(email) 
        user = self.model(email=email,**extra_fields)
        if password:
            user.set_password(password)
        else:
            raise ValueError('The password field must be set')
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        This create_superuser function is used for the create the Admin.

        Args:
            email (email): Email for the Admin login.
            password (text, optional): password for the Admin login. Defaults to None.

        Returns:
            _type_: _description_
        """
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        if password is None:
            raise ValueError('Superuser must have a password')
        return self.create_user(email,password,**extra_fields)
    
    def get_by_natural_key(self, email):
        """
            Retrieve a user from the database using their email address.

            This method looks up a user based on the provided email address,
            which is used as the natural key for identification.

            Args:
                email (str): The email address of the user to retrieve.

            Returns:
                User: The user instance associated with the provided email address.
        """
        return self.get(email=email)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):   
    """
    This class is contains all the required field for the user or admin creation according to there role.
    """ 
    USER = 'user'
    ADMIN = 'admin'
    SUPER_ADMIN = 'superadmin'

    ROLE_CHOICE = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (SUPER_ADMIN, 'superadmin'),
    ]

    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False )
    email = models.EmailField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=20, blank=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICE, default=USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_no']

    def __str__(self) -> str:
        """
        Return the string representation of the CustomUser instance.
        
        This method returns the user's email address, which is used
        as the primary way to represent the user in string format.
        
        Returns:
            str: The email address of the user.
        """
        return self.email
    
    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
        db_table = 'custom_user'  # Custom table name

    # Custom related_name to avoid conflicts

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True
    )

# class Car(models.Model):
#     user = models.ForeignKey(UserLogin, on_delete=models.CASCADE)
#     make_by = models.CharField(max_length=255)
#     model_name = models.CharField(max_length=255)
#     year = models.CharField(max_length=4)
#     vin = models.CharField(max_length=17)
#     status = models.CharField(max_length=8)
#     license_plate = models.CharField(max_length=20)
#     brand_name = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Location(models.Model):
#     location_name = models.CharField(max_length=255)
#     country_code = models.CharField(max_length=3)
#     service_available = models.CharField(max_length=8)

# class ServiceType(models.Model):
#     type_name = models.CharField(max_length=100)
#     status = models.CharField(max_length=8)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)

# class Categories(models.Model):
#     category_name = models.CharField(max_length=100)
#     service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
#     status = models.CharField(max_length=8)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)

# class Services(models.Model):
#     service_title = models.CharField(max_length=255)
#     category = models.ForeignKey(Categories, on_delete=models.CASCADE)
#     service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
#     is_popular = models.BooleanField(default=False)
#     status = models.CharField(max_length=8)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Appointment(models.Model):
#     car = models.ForeignKey(Car, on_delete=models.CASCADE)
#     service = models.ForeignKey(Services, on_delete=models.CASCADE)
#     location = models.ForeignKey(Location, on_delete=models.CASCADE)
#     appointment_date = models.DateTimeField()
#     status = models.CharField(max_length=20)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)

# class Notification(models.Model):
#     user = models.ForeignKey(UserLogin, on_delete=models.CASCADE)
#     notification_message = models.TextField()
#     notification_type = models.CharField(max_length=20)
#     is_read = models.BooleanField(default=False)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)

# class PaymentBill(models.Model):
#     appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_date = models.DateTimeField()
#     payment_method = models.CharField(max_length=20)
#     paymentstatus = models.CharField(max_length=7)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)

# class Referral(models.Model):
#     referrer = models.ForeignKey(UserLogin, on_delete=models.CASCADE)
#     referred_email_id = models.EmailField(max_length=100)
#     referral_date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=7)

# class ServiceCharge(models.Model):
#     service = models.ForeignKey(Services, on_delete=models.CASCADE)
#     effective_date = models.DateField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class SubService(models.Model):
#     service = models.ForeignKey(Services, on_delete=models.CASCADE)
#     selection_type = models.CharField(max_length=8)
#     optional = models.BooleanField()
#     status = models.CharField(max_length=8)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class SubServiceOption(models.Model):
#     title = models.CharField(max_length=255)
#     sub_service = models.ForeignKey(SubService, on_delete=models.CASCADE)
#     option_type = models.CharField(max_length=6)
#     order = models.IntegerField()
#     status = models.CharField(max_length=8)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class UserSavedCar(models.Model):
#     user = models.ForeignKey(UserLogin, on_delete=models.CASCADE)
#     car = models.ForeignKey(Car, on_delete=models.CASCADE)
#     saved_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)