from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'state']

    def create(self, validated_data):
        
        validated_data['username'] = validated_data['first_name'] + "_" + validated_data['last_name']
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = instance.first_name + "_" + instance.last_name
        instance.password = validated_data.get('password', instance.password)
        instance.state = validated_data.get('state', instance.state)
        instance.save()
        return instance
    
class ManagerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Manager
        fields = ['user', 'leasdate']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUserSerializer.create(CustomUserSerializer(), validated_data=user_data)
        admin = Manager.objects.create(user=user, **validated_data)
        return admin
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        user = CustomUserSerializer.update(CustomUserSerializer(), instance=user, validated_data=user_data)
        instance.user = user
        instance.save()
        return instance

class EmployeeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Employee
        fields = ['user', 'manager']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUserSerializer.create(CustomUserSerializer(), validated_data=user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        user = CustomUserSerializer.update(CustomUserSerializer(), instance=user, validated_data=user_data)
        instance.user = user
        instance.save()
        return instance

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['manager', 'id', 'name', 'price']

class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ['id', 'manager', 'employee', 'service', 'date']

class DayServicesSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    service = ServiceTypeSerializer(many=True)

    class Meta:
        model = Service
        fields = ['id', 'manager', 'employee', 'service', 'date']