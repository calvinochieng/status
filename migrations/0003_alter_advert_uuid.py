# Generated by Django 3.2.3 on 2021-06-16 19:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0002_alter_advert_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
