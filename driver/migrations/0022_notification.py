# Generated by Django 2.2.1 on 2019-07-13 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0021_auto_20190704_0137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('identification', models.CharField(max_length=100)),
            ],
        ),
    ]
