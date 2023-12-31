# Generated by Django 3.2.3 on 2021-08-07 21:36

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0019_auto_20210807_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountapproval',
            name='screenshot_img',
        ),
        migrations.AddField(
            model_name='accountapproval',
            name='screenshot',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='approval_screenshot'),
        ),
        migrations.AlterField(
            model_name='jobfeedback',
            name='submitted_views',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
