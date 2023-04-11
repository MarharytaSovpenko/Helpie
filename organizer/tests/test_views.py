from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from organizer.models import Task, Info, Importance, Status
from organizer.views import TaskListView

TASK_URL = reverse("organizer:task-list")
HOME_PAGE_URL = reverse("organizer:index")


class OnlyLoggedIn(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin123"
        )
        self.importance = Importance.objects.create(
            name="low"
        )
        self.status = Status.objects.create(
            name="todo"
        )
        self.info = Info.objects.create(
            task_category="Test Category",
            importance=self.importance,
            details="Test Info",
            delegator="Test",
            status=self.status
        )
        self.info.doers.add(self.user)
        self.task = Task.objects.create(
            description="Test Task"
        )
        self.task.doers.add(self.user)

        self.client.force_login(self.user)


class PublicAccessTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(TASK_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_home_page_with_unauthenticated_user(self):
        response = self.client.get(HOME_PAGE_URL)
        self.assertRedirects(
            response, "/accounts/login/?next=%2F"
        )


class PrivateHomePageTest(OnlyLoggedIn, TestCase):
    def test_index_view_with_authenticated_user(self):
        response = self.client.get(HOME_PAGE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "organizer/index.html")


class PrivateInfoTest(OnlyLoggedIn, TestCase):

    def test_info_list_view(self):
        response = self.client.get(reverse("organizer:info-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Category")

    def test_info_detail_view(self):
        response = self.client.get(
            reverse("organizer:info-detail", args=[self.info.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Info")

    def test_info_create_view(self):
        data = {
            "task_category": "New Category",
            "importance": [self.importance.pk],
            "details": "New Info",
            "delegator": "Test",
            "doers": [self.user.pk],
            "status": [self.status.pk]
        }
        response = self.client.post(
            reverse("organizer:info-create"), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Info.objects.filter(details="New Info").exists())

    def test_info_update_view(self):
        data = {
            "task_category": "Updated Category",
            "importance": [self.importance.pk],
            "details": "Updated Info",
            "delegator": "Test",
            "doers": [self.user.pk],
            "status": [self.status.pk]
        }
        response = self.client.post(
            reverse("organizer:info-update", args=[self.info.id]),
            data=data
        )
        self.assertEqual(response.status_code, 302)
        self.info.refresh_from_db()
        self.assertEqual(self.info.details, "Updated Info")
        self.assertEqual(self.info.task_category, "Updated Category")

    def test_info_delete_view(self):
        response = self.client.post(
            reverse("organizer:info-delete", args=[self.info.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Info.objects.filter(
                task_category="Test Category"
            ).exists()
        )


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

    def test_task_create_view(self):
        url = reverse("organizer:task-create")
        form_data = {
            "description": "test description",
            "doers": [self.user.pk]
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Task.objects.filter(
                description="test description").exists()
        )


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

    def test_update_doer_name(self):
        form_data = {"first_name": "John", "last_name": "Doe"}
        response = self.client.post(
            reverse("organizer:doer-update", args=[self.user.id]),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, HOME_PAGE_URL)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")

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


class ToggleAssignToTaskTest(OnlyLoggedIn, TestCase):

    def test_toggle_assign_to_task(self):
        response = self.client.post(
            reverse_lazy("organizer:toggle-task-assign", args=[self.task.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.tasks.count(), 0)
        response = self.client.post(
            reverse_lazy("organizer:toggle-task-assign", args=[self.task.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.tasks.count(), 1)

    def test_toggle_delete_from_list(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse_lazy(
                "organizer:toggle-delete-from-list",
                args=[self.task.id]
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.tasks.count(), 0)
