from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    """
    This method is used for create a Super user after the first migration and this method is work only once after it refused that task.
    """
    User = get_user_model()
    if User.objects.count() == 0:
        print("Creating superuser...")
        try:
            superAdmin = User.objects.create_superuser(
                email='superuser@gmail.com',
                password='superuser@123',
                first_name="superuser",
                last_name="superuser",
                phone_no="1234567890",
                role='superuser',
                is_staff='True',
                is_superuser='True'
            )
            print("Superuser created successfully.")
        except Exception as e:
            print(f"Failed to create superuser: {str(e)}")