import hashlib
from django.conf import settings
from django.dispatch import receiver
from user_app.models import CustomUser
from django.db.models.signals import post_migrate

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    """
    This method is used for create a Super user after the first migration and this method is work only once after it refused that task.
    """
    try:
        superuser_exists = CustomUser.objects.filter(email=settings.SUPER_USER_EMAIL, role='superuser').exists()
        
        if superuser_exists:
            return
        
        try:
            superAdmin = CustomUser.objects.create_superuser(
                email=settings.SUPER_USER_EMAIL,
                password=settings.SUPER_USER_PASSWORD,
                first_name=settings.SUPER_USER_FIRST_NAME,
                last_name=settings.SUPER_USER_LAST_NAME,
                phone_no=settings.SUPER_USER_PHONE_NO,
                role='superuser',
                remember_token = hashlib.sha256(settings.SUPER_USER_FIRST_NAME.encode()).hexdigest()
            )
        except Exception as e:
            print(f"Failed to create superuser: {str(e)}")
       
    except CustomUser.DoesNotExist:
        pass