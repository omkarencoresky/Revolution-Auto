from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    """
    This method is used for create a Super user after the first migration and this method is work only once after it refused that task.
    """
    try:
        User = get_user_model()
        user = User.objects.get(email=settings.SUPER_USER_EMAIL,role='superuser')
        if not user:
            print("Creating superuser...")
            try:
                superAdmin = User.objects.create_superuser(
                    email=settings.SUPER_USER_EMAIL,
                    password=settings.SUPER_USER_PASSWORD,
                    first_name=settings.SUPER_USER_FIRST_NAME,
                    last_name=settings.SUPER_USER_LAST_NAME,
                    phone_no=settings.SUPER_USER_PHONE_NO,
                    role='superuser',
                    is_staff=True,
                    is_superuser=True
                )
                print("Superuser created successfully.")
            except Exception as e:
                print(f"Failed to create superuser: {str(e)}")
        else:
            print("Super user is already existed")
    except User.DoesNotExist:
        pass