# Generated by Django 5.1.3 on 2024-11-22 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='webhook',
            field=models.URLField(blank=True, null=True),
        ),
    ]
