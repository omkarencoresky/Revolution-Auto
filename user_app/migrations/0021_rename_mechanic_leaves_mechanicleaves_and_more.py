# Generated by Django 5.0.7 on 2024-11-27 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0020_rename_user_combo_package_usercombopackage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Mechanic_leaves',
            new_name='MechanicLeaves',
        ),
        migrations.RenameModel(
            old_name='Service_payment',
            new_name='ServicePayment',
        ),
    ]