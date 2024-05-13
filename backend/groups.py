# from django.contrib.auth.models import Group, Permission
# from rest_framework import permissions

# from django.contrib.contenttypes.models import ContentType

# def create_groups():

#     manager_group, created = Group.objects.get_or_create(name='Manager')
#     employee_group, created = Group.objects.get_or_create(name='Employee')

#     content_type = ContentType.objects.get_for_model(Service)
#     permission = Permission.objects.create(
#         codename='can_manage_services',
#         name='Can Manage Services',
#         content_type=content_type,
#     )
#     manager_group.permissions.add(permission)


# class IsManager(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name='Manager').exists()