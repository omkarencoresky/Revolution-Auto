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