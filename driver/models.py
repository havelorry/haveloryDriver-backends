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