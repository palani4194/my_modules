# Generated by Django 2.0 on 2018-05-17 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_remove_adultdata_fnlwgt'),
    ]

    operations = [
        migrations.AddField(
            model_name='adultdata',
            name='fnl_wgt',
            field=models.IntegerField(default=0),
        ),
    ]
