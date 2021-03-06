from rest_framework import serializers
from .models import Driver,activeLogin, Ride, Notification
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    def create(self,validated_data):
        user=User.objects.create(**validated_data)
        user.save()
        
        return user
    def update(self,instance,validate_data):
        instance.first_name=validate_data.get('first_name',instance.first_name)
        instance.last_name=validate_data.get('last_name',instance.last_name)
        instance.email=validate_data.get('email',instance.email)
        instance.save()
        return instance
    class Meta:
        model=User
        fields='__all__'


class ProfileDetailSerializer(serializers.ModelSerializer):
    def create(self,validated_data):
        driver=Driver.objects.create(**validated_data)
        driver.save()
        return driver
    
    
    def update(self,instance,validate_data):
        instance.address=validate_data.get('address',instance.address)
        instance.mobile=validate_data.get('mobile',instance.mobile)
        instance.vehicle_number=validate_data.get('vehicle_number',instance.vehicle_number)
        instance.locations=validate_data.get('locations',instance.locations)
        instance.age=validate_data.get('age',instance.age)
        
        instance.save()
        return instance
    
    class Meta:
        model=Driver
        fields='__all__'            

class ActiveLoginSerializer(serializers.ModelSerializer):
    def create(self,validated_data):
        driver=activeLogin.objects.create(**validated_data)
        driver.save()
        return driver
    
    def update(self,instance,validate_data):
        instance.active=validate_data.get('active',instance.active)
        instance.location=validate_data.get('location',instance.location)
        instance.status=validate_data.get('status',instance.status)
        
        instance.save()
        return instance
    class Meta:
        model=activeLogin
        fields='__all__'
#class DriverDetailSerializer(serializers.ModelSerializer):
    
class RideSerializer(serializers.ModelSerializer):
    

    def create(self,validated_data):
        print (validated_data)
        ride = Ride.objects.create(**validated_data)
        ride.save()
        return ride


    def update(self,instance,validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    class Meta:
        model =Ride
        fields ='__all__'


class Location(object):
    def __init__(self,  **kwargs):
        for field in ('origin', 'destination'):
            setattr(self,field,kwargs.get(field))






class Coordinatefield(serializers.Field):
     def to_representation(self, value):
          return {
              'latitude':value.latitude,
              'longitude':value.longitude
          }

     def to_internal_value(self, data):
          return {
              'latitude':data['latitude'],
              'longitude':data['longitude'],
          }




class LocationSerializer(serializers.Serializer):
    origin = Coordinatefield(source="*")
    destination = Coordinatefield(source="*")

    def create(self, validated_data):
        return Location(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance,field.value)
        return instance

class RedeDetailSerializer(serializers.Serializer):
    class Meta:
        model =Ride
        fields ='__all__'         




class NotificationSerializer(serializers.ModelSerializer):
    def create(self,validated_data):
       # print ('serializer=',**validated_data)
        notification_done = Notification.objects.create(**validated_data)
        notification_done.save()
        return notification_done

    def update(self,instance,validated_data):
        instance.token = validated_data.get('token', instance.token)
        instance.save()
        return instance 

    class Meta:
        model=Notification
        fields='__all__'