# Generated by Django 3.2.3 on 2021-07-15 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0009_advert_platform'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='client',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
