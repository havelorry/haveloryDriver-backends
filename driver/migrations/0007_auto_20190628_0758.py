# Generated by Django 2.2.1 on 2019-06-28 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0006_activelogin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activelogin',
            name='active',
            field=models.CharField(default=0, max_length=100),
        ),
    ]