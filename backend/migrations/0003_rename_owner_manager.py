# Generated by Django 4.2.3 on 2024-03-13 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20240312_1017'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Owner',
            new_name='Manager',
        ),
    ]
