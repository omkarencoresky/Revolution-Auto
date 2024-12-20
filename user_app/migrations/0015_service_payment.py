# Generated by Django 5.0.7 on 2024-11-18 09:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0014_alter_bookingandquote_car_vno'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service_payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('service_amount', models.IntegerField()),
                ('status', models.CharField(default='pending', max_length=20)),
                ('stripe_payment_intent_id', models.CharField(max_length=255)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='user_app.bookingandquote')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'booking_payment',
            },
        ),
    ]
