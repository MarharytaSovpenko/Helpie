from django.urls import path

from .views import (
    index,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    DoerListView,
    DoerDetailView,
    DoerCreateView,
    DoerUpdateView,
    DoerDeleteView,
    InfoListView,
    InfoCreateView,
    InfoUpdateView,
    InfoDeleteView,
    toggle_assign_to_task,
    InfoDetailView, toggle_delete_from_list,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "info/",
        InfoListView.as_view(),
        name="info-list",
    ),
    path("info/<int:pk>/", InfoDetailView.as_view(), name="info-detail"),
    path(
        "info/create/",
        InfoCreateView.as_view(),
        name="info-create",
    ),
    path(
        "info/<int:pk>/update/",
        InfoUpdateView.as_view(),
        name="info-update",
    ),
    path(
        "info/<int:pk>/delete/",
        InfoDeleteView.as_view(),
        name="info-delete",
    ),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path(
        "tasks/<int:pk>/toggle-assign/",
        toggle_assign_to_task,
        name="toggle-task-assign",
    ),
    path(
        "tasks/<int:pk>/toggle-delete/",
        toggle_delete_from_list,
        name="toggle-delete-from-list",
    ),
    path("doers/", DoerListView.as_view(), name="doer-list"),
    path(
        "doers/<int:pk>/", DoerDetailView.as_view(), name="doer-detail"
    ),
    path("doers/", DoerListView.as_view(), name="doer-list"),
    path(
        "doers/<int:pk>/", DoerDetailView.as_view(), name="doer-detail"
    ),
    path("doers/create/", DoerCreateView.as_view(), name="doer-create"),
    path(
        "doers/<int:pk>/update/",
        DoerUpdateView.as_view(),
        name="doer-update",
    ),
    path(
        "doers/<int:pk>/delete/",
        DoerDeleteView.as_view(),
        name="doer-delete",
    ),
]

app_name = "organizer"
