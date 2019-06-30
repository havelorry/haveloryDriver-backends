from django.db import models
from django.contrib.auth.models import User

class Driver(models.Model):
    mobile=models.BigIntegerField()
    address=models.TextField()
    vehicle_number=models.BigIntegerField()
    #image=models.FileField(upload_to='static/')
    locations=models.TextField()
    age=models.IntegerField()
    username=models.ForeignKey(User,to_field="username",on_delete=models.CASCADE,default="bhole")

    def __str__(self):
        return '%s , %s'%(self.username,self.locations)
class Ride(models.Model):
    customer_id=models.BigIntegerField()
    status=models.IntegerField()
    dest_latitude=models.FloatField()
    dest_logitude=models.FloatField()
    origin_latitude=models.FloatField()
    origin_longitude=models.FloatField()
    origin_string=models.CharField(max_length=100)
    dest_string=models.CharField(max_length=100)    

    driver_id=models.IntegerField()

class activeLogin(models.Model):
    username=models.ForeignKey(User,to_field="username",on_delete=models.CASCADE,default="bhole",unique=True)
    active=models.CharField(max_length=100,default=0)
    latitude=models.FloatField(default=0)
    longitude=models.FloatField(default=0)
