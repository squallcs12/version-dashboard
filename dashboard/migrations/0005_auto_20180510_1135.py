# Generated by Django 2.0.5 on 2018-05-10 11:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0004_auto_20180509_1535'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='servicedeploy',
            unique_together={('name', 'environment', 'user')},
        ),
    ]
