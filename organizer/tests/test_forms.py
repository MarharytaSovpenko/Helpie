from django.test import TestCase

from organizer.forms import DoerCreationForm


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
