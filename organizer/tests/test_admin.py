from django.contrib.auth import get_user_model
from django.test import TestCase


class AdminPanelTest(TestCase):

    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="adminmag",
            password="minadv123"
        )
        self.client.force_login(self.admin_user)
        self.doer = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="testi",
            last_name="testy",
        )
