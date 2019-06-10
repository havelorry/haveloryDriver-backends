from rest_framework import serializers
from .models import Driver
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    def create(self,validated_data):
        user=User.objects.create(**validated_data)
        user.save()
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model=User
        fields='__all__'

class ProfileDetailSerializer(serializers.ModelSerializer):
    def create(self,validated_data):
        driver=Driver.objects.create(**validated_data)
        driver.save()
        return driver
    class Meta:
        model=Driver
        fields='__all__'            

#class DriverDetailSerializer(serializers.ModelSerializer):
    