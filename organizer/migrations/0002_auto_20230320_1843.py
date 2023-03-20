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
        password="minadv12",
    )
    doer_model.objects.create(
        username="Alex",
        email="alex@ukr.net",
        password="minadv123",
    )

    info_model = apps.get_model('organizer', 'Info')
    info_model.objects.create(
        task_category="shopping",
        importance=4,
        details="bananas 1kg and oranges 2kg",
        delegator="Maggie",
        doers=[1, 2],
        status=2
    )
    info_model.objects.create(
        task_category="birthday",
        importance=1,
        details="book a table in the children's cafe and buy a present for Malya",
        delegator="Maggie",
        doers=[1, 2],
        status=2
    )


class Migration(migrations.Migration):
    dependencies = [
        ("organizer", "0001_initial"),
    ]

    operations = [migrations.RunPython(load_initial_data)]
