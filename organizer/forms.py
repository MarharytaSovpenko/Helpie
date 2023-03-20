from typing import Optional

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from organizer.models import Info, Doer, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('description',)


class DoerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Doer
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
        )


class DoerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"})
    )


class DoerUpdateForm(forms.ModelForm):
    class Meta:
        model = Doer
        fields = ["first_name", "last_name"]

    def clean_license_number(self) -> Optional[str]:
        return self.cleaned_data["first_name", "last_name"]


class TaskSearchForm(forms.Form):
    description = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search"})
    )


class InfoForm(forms.ModelForm):
    delegator = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Please type your username or full name"
        })
    )
    doers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Info
        fields = "__all__"


class InfoSearchForm(forms.Form):
    task_category = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by task category"})
    )
