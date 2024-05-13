from django.db import migrations

def create_groups_and_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Service = apps.get_model('backend', 'Service')  # replace 'your_app_name' with your actual app name

    manager_group, created = Group.objects.get_or_create(name='Manager')
    employee_group, created = Group.objects.get_or_create(name='Employee')

    content_type = ContentType.objects.get_for_model(Service)
    permission = Permission.objects.create(
       codename='can_manage_services',
       name='Can Manage Services',
       content_type=content_type,
    )
    manager_group.permissions.add(permission)

class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions),
    ]
