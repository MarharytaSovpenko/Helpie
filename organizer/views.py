from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Doer, Task, Info
from .forms import (
    TaskForm,
    TaskSearchForm,
    DoerCreationForm,
    DoerSearchForm,
    InfoForm,
    InfoSearchForm,
    DoerUpdateForm,
)


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""

    doer = Doer.objects.get(id=request.user.id)
    num_tasks_to_do = doer.tasks.count()

    context = {
        "num_tasks_to_do": num_tasks_to_do,
    }

    return render(request, "organizer/index.html", context=context)


class InfoListView(LoginRequiredMixin, generic.ListView):
    model = Info
    context_object_name = "info_list"
    template_name = "organizer/info_list.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(InfoListView, self).get_context_data(**kwargs)
        task_category = self.request.GET.get("task_category", "")
        context["search_form"] = InfoSearchForm(initial={
            "task_category": task_category
        })

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Info.objects.select_related("importance", "status")
        form = InfoSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                task_category__icontains=form.cleaned_data["task_category"]
            )

        return queryset


class InfoDetailView(LoginRequiredMixin, generic.DetailView):
    model = Info


class InfoCreateView(LoginRequiredMixin, generic.CreateView):
    model = Info
    form_class = InfoForm
    success_url = reverse_lazy("organizer:info-list")


class InfoUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Info
    form_class = InfoForm
    success_url = reverse_lazy("organizer:info-list")


class InfoDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Info
    success_url = reverse_lazy("organizer:info-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(TaskListView, self).get_context_data(**kwargs)
        description = self.request.GET.get("description", "")
        context["search_form"] = TaskSearchForm(initial={
            "description": description
        })

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Task.objects.all()
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                description__icontains=form.cleaned_data["description"]
            )

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("organizer:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("organizer:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("organizer:task-list")


class DoerListView(LoginRequiredMixin, generic.ListView):
    model = Doer
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(DoerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = DoerSearchForm(initial={
            "username": username
        })

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Doer.objects.prefetch_related("tasks", "info__importance", "info__status")
        form = DoerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return queryset


class DoerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Doer


class DoerCreateView(generic.CreateView):
    model = Doer
    form_class = DoerCreationForm
    success_url = reverse_lazy("organizer:index")


class DoerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Doer
    form_class = DoerUpdateForm
    template_name = "organizer/doer_update_name_form.html"
    success_url = reverse_lazy("organizer:index")


class DoerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Doer
    success_url = reverse_lazy("organizer:index")


@login_required
def toggle_assign_to_task(request: HttpRequest, pk: int) -> HttpResponse:
    doer = Doer.objects.get(id=request.user.id)
    if (
            Task.objects.get(id=pk) in doer.tasks.all()
    ):
        doer.tasks.remove(pk)
    else:
        doer.tasks.add(pk)
    return HttpResponseRedirect(reverse_lazy("organizer:task-list"))


@login_required
def toggle_delete_from_list(request: HttpRequest, pk: int) -> HttpResponse:
    doer = Doer.objects.get(id=request.user.id)
    if (
            Task.objects.get(id=pk) in doer.tasks.all()
    ):
        doer.tasks.remove(pk)
    return HttpResponseRedirect(reverse_lazy("organizer:doer-detail", kwargs={'pk': doer.id}))
