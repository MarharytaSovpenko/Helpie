from django.db import migrations


def load_initial_data(apps, schema_editor):
    importance_model = apps.get_model('organizer', 'Importance')
    status_model = apps.get_model('organizer', 'Status')
    doer_model = apps.get_model('organizer', 'Doer')

    doer1 = doer_model.objects.get(pk=1)
    doer2 = doer_model.objects.get(pk=2)
    importance1 = importance_model.objects.get(pk=1)
    importance4 = importance_model.objects.get(pk=4)
    status2 = status_model.objects.get(pk=2)

    info_model = apps.get_model('organizer', 'Info')
    info_1 = info_model.objects.create(
        task_category="shopping",
        importance=importance4,
        details="bananas 1kg and oranges 2kg",
        delegator="Maggie",
        status=status2
    )
    info_1.doers.add(doer1, doer2)

    info_2 = info_model.objects.create(
        task_category="birthday",
        importance=importance1,
        details="book a table in the children's cafe and buy a present for Malya",
        delegator="Maggie",
        status=status2
    )
    info_2.doers.add(doer1, doer2)


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("organizer", "0002_auto_20230320_1843"),
    ]

    operations = [migrations.RunPython(load_initial_data, reverse_func)]
