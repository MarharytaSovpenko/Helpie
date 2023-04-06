from django.contrib.auth import get_user_model
from django.test import TestCase

from organizer.models import Importance, Info, Status


class ModelTests(TestCase):
    def test_importance_str(self):
        importance = Importance.objects.create(
            name="test"
        )

        self.assertEqual(
            str(importance),
            importance.name
        )

    def test_doer_str(self):
        doer = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="testi",
            last_name="testy"
        )

        self.assertEqual(
            str(doer),
            doer.username
        )

    def test_info_str(self):
        importance = Importance.objects.create(
            name="no"
        )
        status = Status.objects.create(
            name="no"
        )

        info = Info.objects.create(
            task_category="shopping",
            importance=importance,
            details="apples and bananas",
            delegator="Maggie",
            status=status
        )

        self.assertEqual(str(info), f"{info.task_category} ({info.importance})")
