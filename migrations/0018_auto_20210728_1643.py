# Generated by Django 3.2.3 on 2021-07-28 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0017_auto_20210726_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountapproval',
            name='screenshot',
        ),
        migrations.AddField(
            model_name='accountapproval',
            name='screenshot_img',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='account_approval media'),
        ),
    ]
