# Generated by Django 5.0.7 on 2024-12-12 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0035_alter_forgetpasswordtracking_attempt_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='forgetpasswordtracking',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-12-12 18:41:57.618079+05:30'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='forgetpasswordtracking',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]