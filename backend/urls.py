from django.urls import include, path 
from .views import * 
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'users', UserView , basename='users')
router.register(r'employee', EmployeeView, basename='employees')
router.register(r'manager', ManagerView, basename='admins')
router.register(r'servicetype', ServiceTypeView, basename='servicetypes')
router.register(r'service', ServiceView, basename='services')
router.register(r'daylist', DayServiceView, basename='daylists')
urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]