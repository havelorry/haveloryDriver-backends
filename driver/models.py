from django.db import models
from django.contrib.auth.models import User

AVAILABLE = 'available'
BUSY = 'busy'

class Driver(models.Model):
    mobile=models.BigIntegerField()
    address=models.TextField()
    vehicle_number=models.BigIntegerField()
    #image=models.FileField(upload_to='static/')
    locations=models.TextField()
    age=models.IntegerField()
    workers = models.IntegerField(max_length=2, default=1)
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
    fare = models.FloatField(max_length=5,default=0.0)
    driver_id=models.IntegerField()


class activeLogin(models.Model):
    username=models.ForeignKey(User,to_field="username",on_delete=models.CASCADE,default="bhole",unique=True,)
    active=models.CharField(max_length=100,default=0)
    status=models.CharField(max_length=40,default=AVAILABLE)
    location=models.CharField(max_length=100,null=True)

    def __str__(self):
        return "%s --> %s"%(self.location,self.username)