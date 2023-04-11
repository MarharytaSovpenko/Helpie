from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Importance(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Doer(AbstractUser):
    def __str__(self) -> str:
        return self.username

    def get_absolute_url(self):
        return reverse("organizer:doer-detail", kwargs={"pk": self.pk})


class Task(models.Model):
    description = models.CharField(max_length=255)
    doers = models.ManyToManyField(Doer, related_name="tasks")

    def __str__(self) -> str:
        return self.description

    class Meta:
        ordering = ["description"]


class Info(models.Model):
    task_category = models.CharField(max_length=255)
    importance = models.ForeignKey(Importance, on_delete=models.CASCADE)
    details = models.CharField(max_length=700)
    delegator = models.CharField(max_length=255)
    doers = models.ManyToManyField(Doer, related_name="info")
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "info"
        verbose_name_plural = "info"
        ordering = ["importance__id"]

    def __str__(self) -> str:
        return f"{self.task_category} ({self.importance})"
