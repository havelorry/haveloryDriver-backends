# Generated by Django 2.2.1 on 2019-07-04 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0019_auto_20190704_0101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ride',
            name='driver_id',
        ),
        migrations.AddField(
            model_name='ride',
            name='driver_id',
            field=models.ManyToManyField(to='driver.Driver'),
        ),
    ]
