from django.contrib.auth.models import User
from django.db import migrations


def fill_user_table(apps, schema_editor):
    """
    Create users with id from 1 to 2. It is better to use bulk_create but in Django only create_user encrypt password.
    """
    [User.objects.create_user(id=i, username=f'user_{i}', password='password') for i in range(1, 201)]


def delete_users(apps, schema_editor):
    """Delete all users."""
    User.objects.all().delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunPython(fill_user_table, delete_users)
    ]
