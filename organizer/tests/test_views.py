from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse

from organizer.models import Task
from organizer.views import TaskListView

TASK_URL = reverse("organizer:task-list")


class OnlyLoggedIn(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin123"
        )

        self.client.force_login(self.user)


class PublicTaskTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(TASK_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateTaskTest(OnlyLoggedIn, TestCase):

    def test_retrieve_tasks(self) -> None:
        Task.objects.create(
            description="learn Python"
        )
        Task.objects.create(
            description="learn JavaScript"
        )
        response = self.client.get(TASK_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "organizer/task_list.html")

    def test_get_queryset(self):
        Task.objects.create(
            description="learn Python"
        )
        Task.objects.create(
            description="learn JavaScript"
        )
        description = "Python"
        request = RequestFactory().get("organizer:task-list")
        request.GET = {"description": description}
        view = TaskListView()
        view.request = request
        manufacturers = Task.objects.all()

        queryset = view.get_queryset()

        self.assertQuerysetEqual(queryset, (manufacturers.filter(
            description__icontains=description
        )))


class PrivateDoerTest(OnlyLoggedIn, TestCase):

    def test_create_doer(self):
        form_data = {
            "username": "test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "testi",
            "last_name": "testy"
        }
        self.client.post(reverse("organizer:doer-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])

    def test_delete_doer(self):
        doer = get_user_model().objects.create(
            username="not_admin.user",
            first_name="Not Admin",
            last_name="User",
            password="1qazcde3",
        )
        response = self.client.post(
            reverse("organizer:doer-delete", kwargs={"pk": doer.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=doer.id).exists()
        )
