# Generated by Django 5.0.7 on 2024-11-19 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0016_service_payment_payment_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='service_payment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-11-08 14:54:53.300849+05:30'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service_payment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]