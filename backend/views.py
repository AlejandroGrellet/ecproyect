from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from datetime import datetime  # Add this line

from .models import *
from .serializers import *

class UserView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            # Allow anyone to create a user
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManagerView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

class EmployeeView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        manager_id = self.request.query_params.get('manager_id', None)
        if manager_id is not None:
            return self.queryset.filter(manager=manager_id)
        return super().get_queryset()

    def destroy(self, request, *args, **kwargs):
        employee_id = kwargs.get('pk')
        user = CustomUser.objects.filter(id=employee_id)
        user.delete()
        return Response({"detail": "Deleted"}, status=status.HTTP_204_NO_CONTENT)

class ServiceTypeView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer

    def get_queryset(self):
        manager_id = self.request.query_params.get('manager_id', None)
        if manager_id is not None:
            return self.queryset.filter(manager=manager_id)
        return super().get_queryset()

class ServiceView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class DayServiceView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    queryset = Service.objects.all()
    serializer_class = DayServicesSerializer

    def list(self, request, *args, **kwargs):
        date_str = request.query_params.get('date', None)
        employee_id = request.query_params.get('employee_id', None)
        manager_id = request.query_params.get('manager_id', None)
        if date_str is not None:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if employee_id is not None:
                queryset = self.queryset.filter(manager=manager_id, employee=employee_id, date__date=date)
            else:
                queryset = self.queryset.filter(manager=manager_id, date__date=date)
        else:
            if employee_id is not None:
                queryset = self.queryset.filter(manager=manager_id, employee=employee_id)
            else:
                queryset = self.queryset.filter(manager=manager_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class LoginView(APIView):
    permission_classes = [AllowAny]

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
            return Response({"error": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"success": "Logged out"}, status=status.HTTP_200_OK)

# from django.http import HttpResponse
# from django.contrib.auth import authenticate, login
# from django.utils import timezone
# from datetime import datetime, time, date

# from rest_framework.views import APIView
# from rest_framework import viewsets

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token

# from .models import *
# from .serializers import *

# class UserView(viewsets.ModelViewSet):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer

#     def get_permissions(self):
#         if self.request.method in ['POST']:
#             return [AllowAny()]
#         return [IsAuthenticated()]

#     def get(self, request):
#         users = CustomUser.objects.all()
#         serializer = CustomUserSerializer(users, many=True)
#         return HttpResponse(serializer.data)

#     def post (self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(serializer.data)
#         return HttpResponse(serializer.errors)
    
#     def put(self, request):
#         user = CustomUser.objects.get(id=request.data['id'])
#         serializer = CustomUserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(serializer.data)
#         return HttpResponse(serializer.errors)
     
# class ManagerView(viewsets.ModelViewSet):
#     queryset = Manager.objects.all()
#     serializer_class = ManagerSerializer

#     def get(self, request):
#         admins = Manager.objects.all()
#         serializer = ManagerSerializer(admins, many=True)
#         return HttpResponse(serializer.data)
    
#     def post(self, request):
#         serializer = ManagerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(serializer.data)
#         return HttpResponse(serializer.errors)
    
#     def put(self, request, pk):
#         admin = Manager.objects.get(pk=pk)
#         serializer = ManagerSerializer(admin, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(serializer.data)
#         return HttpResponse(serializer.errors)

# class EmployeeView(viewsets.ModelViewSet):

#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer

#     def get_queryset(self):
#         queryset = Employee.objects.all()
#         manager_id = self.request.query_params.get('manager_id', None)
#         if manager_id is not None:
#             queryset = queryset.filter(manager=manager_id)
#         return queryset
        
#     def post(self, request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(serializer.data)
#         return HttpResponse(serializer.errors)
    
#     def put(self, request, pk):
#         employee = Employee.objects.get(pk=pk)
#         serializer = EmployeeSerializer(employee, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(serializer.data)
#         return HttpResponse(serializer.errors)
    
#     def delete(self, request):
#         manager_id = self.request.query_params.get('manager_id', None)
#         employee_id = self.request.query_params.get('employee_id', None)
#         # employee = Employee.objects.get(pk=employee_id)
#         user = CustomUser.objects.filter(id=employee_id)
#         # employee.delete()
#         user.delete()
#         return HttpResponse("Deleted")
    
# class ServiceTypeView(viewsets.ModelViewSet):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]  
#     queryset = ServiceType.objects.all()
#     serializer_class = ServiceTypeSerializer

#     def get_queryset(self):
#         queryset = ServiceType.objects.all()
#         manager_id = self.request.query_params.get('manager_id', None)
#         if manager_id is not None:
#             queryset = queryset.filter(manager=manager_id)
#         return queryset
    
#     def post(self, request):
#         manager_id = self.request.query_params.get('manager_id', None)
#         serializer = ServiceTypeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(serializer.data)
#         return HttpResponse(serializer.errors)
    
#     def put(self, request):
#         manager_id = self.request.query_params.get('manager_id', None)
#         service_id = self.request.query_params.get('service_id', None)
#         service_type = ServiceType.objects.get(id=service_id, manager=manager_id)
#         serializer = ServiceTypeSerializer(service_type, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(serializer.data)
#         return HttpResponse(serializer.errors)
#     def delete(self, request):
#         manager_id = self.request.query_params.get('manager_id', None)
#         service_id = self.request.query_params.get('service_id', None)
#         service_type = ServiceType.objects.get(id=service_id, manager=manager_id)
#         service_type.delete()
#         return HttpResponse("Deleted")

# class ServiceView(viewsets.ModelViewSet):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]  
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer

#     def get(self, request):
#         services = Service.objects.all()
#         serializer = ServiceSerializer(services, many=True)
#         return HttpResponse(serializer.data)
    
#     def post(self, request):
#         serializer = ServiceSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(serializer.data)
#         return HttpResponse(serializer.errors)
    
#     def put(self, request, pk):
#         service = Service.objects.get(pk=pk)
#         serializer = ServiceSerializer(service, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(serializer.data)
#         return HttpResponse(serializer.errors)
    
#     def delete(self, request, pk):
#         service = Service.objects.get(pk=pk)
#         service.delete()
#         return HttpResponse("Deleted")

# class DayServiceView(viewsets.ModelViewSet):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated] 
    
#     queryset = Service.objects.all()
#     serializer_class = DayServicesSerializer

#     def list(self, request, *args, **kwargs):
#         date_str = self.request.query_params.get('date', None)
#         employee_id = request.query_params.get('employee_id', None)
#         manager_id = request.query_params.get('manager_id', None)
#         if date_str is not None:
#             date = datetime.strptime(date_str, "%Y-%m-%d").date()  # convert string to date
#             if employee_id is not None:
#                 queryset = Service.objects.filter(manager=manager_id, employee=employee_id, date__date=date)
#             else:
#                 # select all services for today order by name of the employee
#                 queryset = Service.objects.filter(manager=manager_id, date__date=date)  # filter by date
#         else:
#             if employee_id is not None:
#                 queryset = Service.objects.filter(manager=manager_id, employee=employee_id)
#             else:
#                 # select all services for today order by name of the employee
#                 queryset = Service.objects.filter(manager=manager_id)  
#         serializer = DayServicesSerializer(queryset, many=True)
#         return Response(serializer.data)       

# class LoginView(APIView):
#     # permission_classes = [AllowAny]

#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             if hasattr(user, 'employee'):
#                 employee = Employee.objects.get(user=user)
#                 token, created = Token.objects.get_or_create(user=user)
#                 return Response({"token": token.key, "employee_id": employee.user.id,
#                                   "employee_first_name": employee.user.first_name,
#                                   "employee_last_name": employee.user.last_name,
#                                   "manager_id": employee.manager.user.id})
#             elif hasattr(user, 'manager'):
#                 manager = Manager.objects.get(user=user)
#                 token, created = Token.objects.get_or_create(user=user)
#                 return Response({"token": token.key, 
#                                  "manager_first_name": manager.user.first_name, 
#                                  "manager_last_name": manager.user.last_name,
#                                  "manager_id": manager.user.id})
#         else:
#             return Response({"error": "Login failed"})
    
# class LogoutView(APIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAuthenticated]

#     def post(self, request):
#         # request.user.auth_token.delete()
#         return Response({"success": "Logged out"})
    
