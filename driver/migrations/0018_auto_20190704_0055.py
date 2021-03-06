# Generated by Django 2.2.1 on 2019-07-04 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0017_merge_20190703_0637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ride',
            old_name='dest_logitude',
            new_name='dest_longitude',
        ),
        migrations.RemoveField(
            model_name='activelogin',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='activelogin',
            name='longitude',
        ),
        migrations.AddField(
            model_name='activelogin',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='driver',
            name='workers',
            field=models.IntegerField(default=1),
        ),
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
