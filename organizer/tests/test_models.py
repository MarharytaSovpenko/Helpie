from django.contrib.auth import get_user_model
from django.test import TestCase

from organizer.models import Importance, Info, Status


class ModelTests(TestCase):
    def setUp(self):
        self.importance = Importance.objects.create(name="high")
        self.doer = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="testi",
            last_name="testy"
        )
        self.status = Status.objects.create(name="no")
        self.info = Info.objects.create(
            task_category="shopping",
            importance=self.importance,
            details="apples and bananas",
            delegator="Maggie",
            status=self.status
        )

    def test_importance_str(self):
        self.assertEqual(str(self.importance), self.importance.name)

    def test_doer_str(self):
        self.assertEqual(str(self.doer), self.doer.username)

    def test_info_str(self):
        self.assertEqual(
            str(self.info),
            f"{self.info.task_category} ({self.info.importance})"
        )
