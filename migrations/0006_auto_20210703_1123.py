# Generated by Django 3.2.3 on 2021-07-03 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0005_auto_20210625_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='percentage',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='jobfeedback',
            name='income',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]