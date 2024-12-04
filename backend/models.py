from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group




class State(models.TextChoices):
    ACTIVATED = "A", "Activated"
    DEACTIVATED = "D", "Deactivated"



class CustomUser(AbstractUser):
    state = models.CharField(max_length=1, choices=State.choices, default=State.ACTIVATED)

    def __str__(self):
        return  self.first_name + " " + self.last_name
    
class Manager(models.Model):
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE)
    leasdate = models.DateField(default=None)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        manager_group = Group.objects.get(name='Manager')
        self.user.groups.add(manager_group)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    
class Employee(models.Model):
    
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE)
    manager= models.ForeignKey(Manager, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        employee_group = Group.objects.get(name='Employee')
        self.user.groups.add(employee_group)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class ServiceType(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.name + "// " + str(self.price)

class Service(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    service = models.ManyToManyField(ServiceType)
    date = models.DateTimeField()

    def __str__(self):
        service_names = ", ".join([service.name for service in self.service.all()])
        return self.employee.user.first_name + " " + self.employee.user.last_name + " " + str(self.date) + " " + service_names
