# Generated by Django 5.0.7 on 2024-12-10 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0031_forgetpasswordtracking'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='forgetpasswordtracking',
            table='forget_password-tracking',
        ),
    ]
