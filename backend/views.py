
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.utils import timezone
from datetime import datetime, time, date

from rest_framework.views import APIView
from rest_framework import viewsets

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import *
from .serializers import *

class UserView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return HttpResponse(serializer.data)

    def post (self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data)
        return HttpResponse(serializer.errors)
    
    def put(self, request):
        user = CustomUser.objects.get(id=request.data['id'])
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data)
        return HttpResponse(serializer.errors)
     
class ManagerView(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    def get(self, request):
        admins = Manager.objects.all()
        serializer = ManagerSerializer(admins, many=True)
        return HttpResponse(serializer.data)
    
    def post(self, request):
        serializer = ManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data)
        return HttpResponse(serializer.errors)
    
    def put(self, request, pk):
        admin = Manager.objects.get(pk=pk)
        serializer = ManagerSerializer(admin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data)
        return HttpResponse(serializer.errors)

class EmployeeView(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        queryset = Employee.objects.all()
        manager_id = self.request.query_params.get('manager_id', None)
        if manager_id is not None:
            queryset = queryset.filter(manager=manager_id)
        return queryset
        
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data)
        return HttpResponse(serializer.errors)
    
    def put(self, request, pk):
        employee = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data)
        return HttpResponse(serializer.errors)
    
    def delete(self, request):
        manager_id = self.request.query_params.get('manager_id', None)
        employee_id = self.request.query_params.get('employee_id', None)
        # employee = Employee.objects.get(pk=employee_id)
        user = CustomUser.objects.filter(id=employee_id)
        # employee.delete()
        user.delete()
        return HttpResponse("Deleted")
    
class ServiceTypeView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer

    def get_queryset(self):
        queryset = ServiceType.objects.all()
        manager_id = self.request.query_params.get('manager_id', None)
        if manager_id is not None:
            queryset = queryset.filter(manager=manager_id)
        return queryset
    
    def post(self, request):
        manager_id = self.request.query_params.get('manager_id', None)
        serializer = ServiceTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data)
        return HttpResponse(serializer.errors)
    
    def put(self, request):
        manager_id = self.request.query_params.get('manager_id', None)
        service_id = self.request.query_params.get('service_id', None)
        service_type = ServiceType.objects.get(id=service_id, manager=manager_id)
        serializer = ServiceTypeSerializer(service_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data)
        return HttpResponse(serializer.errors)
    def delete(self, request):
        manager_id = self.request.query_params.get('manager_id', None)
        service_id = self.request.query_params.get('service_id', None)
        service_type = ServiceType.objects.get(id=service_id, manager=manager_id)
        service_type.delete()
        return HttpResponse("Deleted")

class ServiceView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return HttpResponse(serializer.data)
    
    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data)
        return HttpResponse(serializer.errors)
    
    def put(self, request, pk):
        service = Service.objects.get(pk=pk)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data)
        return HttpResponse(serializer.errors)
    
    def delete(self, request, pk):
        service = Service.objects.get(pk=pk)
        service.delete()
        return HttpResponse("Deleted")

class DayServiceView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    
    queryset = Service.objects.all()
    serializer_class = DayServicesSerializer

    def list(self, request, *args, **kwargs):
        date = self.request.query_params.get('date', None)
        employee_id = request.query_params.get('employee_id', None)
        manager_id = request.query_params.get('manager_id', None)
        if date is not None:
            if employee_id is not None:
                queryset = Service.objects.filter(manager=manager_id,employee=employee_id, date=date)
            else:
                # select all services for today order by name of the employee
                queryset = Service.objects.filter(manager=manager_id,date=date) #.order_by('employee__user__first_name')
                # queryset = Service.objects.all().order_by()
        else:
            queryset = Service.objects.filter(manager=manager_id)
        serializer = DayServicesSerializer(queryset, many=True)
        return Response(serializer.data)        

class LoginView(APIView):
    # permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if hasattr(user, 'employee'):
                employee = Employee.objects.get(user=user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key, "employee_id": employee.user.id,
                                  "employee_first_name": employee.user.first_name,
                                  "employee_last_name": employee.user.last_name,
                                  "manager_id": employee.manager.user.id})
            elif hasattr(user, 'manager'):
                manager = Manager.objects.get(user=user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key, 
                                 "manager_first_name": manager.user.first_name, 
                                 "manager_last_name": manager.user.last_name,
                                 "manager_id": manager.user.id})
        else:
            return Response({"error": "Login failed"})
    
class LogoutView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        # request.user.auth_token.delete()
        return Response({"success": "Logged out"})
    
