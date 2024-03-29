from django.contrib.auth.hashers import make_password
from django.db import migrations


def load_initial_data(apps, schema_editor):
    importance_model = apps.get_model('organizer', 'Importance')
    importance_model.objects.create(name="very important")
    importance_model.objects.create(name="fairly important")
    importance_model.objects.create(name="important")
    importance_model.objects.create(name="slightly important")
    importance_model.objects.create(name="not important")

    status_model = apps.get_model('organizer', 'Status')
    status_model.objects.create(name="Done")
    status_model.objects.create(name="Not done yet")

    task_model = apps.get_model('organizer', 'Task')
    task_model.objects.create(description="go shopping")
    task_model.objects.create(description="take children to school")
    task_model.objects.create(description="cook breakfast")
    task_model.objects.create(description="cook lunch")
    task_model.objects.create(description="cook dinner")
    task_model.objects.create(description="wash the floor")
    task_model.objects.create(description="wash the kitchen")
    task_model.objects.create(description="open a new bank account")
    task_model.objects.create(description="send enquiry to kindergarten")
    task_model.objects.create(description="teach children English")
    task_model.objects.create(description="teach French")
    task_model.objects.create(description="learn Czech")
    task_model.objects.create(description="organize a birthday party")
    task_model.objects.create(description="go to work")

    doer_model = apps.get_model('organizer', 'Doer')
    doer_model.objects.create(
        username="adminmag",
        email="admi@ukr.net",
        password=make_password("minadv12")
    )
    doer_model.objects.create(
        username="Alex",
        email="alex@ukr.net",
        password=make_password("minadv123")
    )


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("organizer", "0001_initial"),
    ]

    operations = [migrations.RunPython(load_initial_data, reverse_func)]
