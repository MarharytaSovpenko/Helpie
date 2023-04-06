from django.test import TestCase

from organizer.forms import DoerCreationForm, DoerUpdateForm
from organizer.models import Doer


class FormTest(TestCase):
    def test_doer_creation_form_with_specific_fields_is_valid(self):
        form_data = {
            "username": "test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "testi",
            "last_name": "testy",
        }
        form = DoerCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_valid_form(self):
        doer = Doer.objects.create(first_name="John", last_name="Doe")
        data = {"first_name": "Jane", "last_name": "Doe"}
        form = DoerUpdateForm(data=data, instance=doer)
        self.assertTrue(form.is_valid())
        doer = form.save()
        self.assertEqual(doer.first_name, "Jane")
        self.assertEqual(doer.last_name, "Doe")
