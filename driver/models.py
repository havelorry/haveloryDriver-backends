from django.db import models
from django.contrib.auth.models import User
import datetime
from django.forms.models import model_to_dict
from django.db.models import Q
AVAILABLE = 'available'
BUSY = 'busy'

class Driver(models.Model):
    mobile=models.BigIntegerField()
    address=models.TextField()
    vehicle_number=models.BigIntegerField()
    #image=models.FileField(upload_to='static/')
    locations=models.TextField()
    profilePic = models.CharField(max_length=255,default="")
    age=models.IntegerField()
    workers = models.IntegerField(default=1)
    username=models.ForeignKey(User,to_field="username",on_delete=models.CASCADE,default="bhole")

    def __str__(self):
        return '%s , %s'%(self.username,self.locations)

t = lambda x: dict({
                1:'CREATED',
                2:'ACCEPTED',
                3:'DISPATCHED',
                4:'CANCELLED',
                5:'COMPLETED'
            }).get(x)


rev = lambda x: dict({
    'CREATED'   :1,  
    'ACCEPTED'  :2, 
    'DISPATCHED':3,
    'CANCELLED' :4,
    'COMPLETED' :5
}).get(x)

class Ride(models.Model):
    customer_id=models.BigIntegerField()
    status=models.IntegerField()
    dest_latitude=models.FloatField()
    dest_longitude=models.FloatField()
    origin_latitude=models.FloatField()
    origin_longitude=models.FloatField()
    origin_string=models.CharField(max_length=100)
    dest_string=models.CharField(max_length=100)    
    fare = models.FloatField(max_length=5,default=0.0)
    driver_id=models.IntegerField(default=3)
    is_scheduled = models.BooleanField(default=False)
    extra = models.CharField(max_length=245,default="NULL")    
    date = models.DateField(default=datetime.date.today)
    def toJson(self):

        dictionary = model_to_dict(self) 
        d = {**dictionary,'status': t(
            float(
                dictionary.get('status')
            )
        )}
        return d

    def __str__(self):
        return '%s , %s'%(self.customer_id,self.status)

    @classmethod
    def get_driver_rides(self,driver,flag):
        return Ride.objects.filter(
            Q(driver_id=rev(flag)),
            Q(status=flag)
        )

    @classmethod
    def get_customer_rides(self,customer):
        return Ride.objects.filter(
            Q(customer_id = customer)
        )

    @classmethod
    def get_driver_earnings(self , driverId , Type=5):
        rides = Ride.objects.filter(
                Q(driver_id = driverId),
                Q(status = Type)
            )

        summary = [ model_to_dict(x).get('fare') for x in rides]
        total = sum(summary,0)

        report = {
            'summary':[ x.toJson() for x in list(rides)],
            'total':total
        }

        return report
        

class activeLogin(models.Model):
    username=models.ForeignKey(User,to_field="username",on_delete=models.CASCADE,default="bhole",unique=True,)
    active=models.CharField(max_length=100,default=0)
    status=models.CharField(max_length=40,default=AVAILABLE)
    location=models.CharField(max_length=100,null=True)

    def __str__(self):
        return "%s --> %s"%(self.location,self.username)

    

class AppSetting(models.Model):
    name  = models.CharField(max_length = 55)
    value = models.PositiveIntegerField(default=0)


    def __str__(self):
        return "%s %d"%(self.name,self.value)
        


class Notification(models.Model):
    token=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    identification=models.CharField(max_length=100)
    def __str__(self):
        return "%s %s"%(self.username ,self.token)