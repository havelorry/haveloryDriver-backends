from rest_framework import serializers
from .models import Driver,activeLogin
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    def create(self,validated_data):
        user=User.objects.create(**validated_data)
        user.save()
        user.set_password(validated_data['password'])
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
        instance.latitude=validate_data.get('latitude',instance.latitude)
        instance.longitude=validate_data.get('longitude',instance.longitude)
        
        instance.save()
        return instance
    class Meta:
        model=activeLogin
        fields='__all__'
#class DriverDetailSerializer(serializers.ModelSerializer):
    