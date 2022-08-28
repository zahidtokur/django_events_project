from django.utils import timezone
from datetime import timedelta
from django.test import TestCase

from core.forms import EventForm

class EventFormTestCase(TestCase):

    def test_valid_form(self):
        # a date in the future
        date = timezone.now() + timedelta(days=3)
        data = {
            "title": "event title",
            "description": "event description",
            "date": date.strftime("%Y-%m-%d")
        }
        form = EventForm(data=data)
        self.assertTrue(form.is_valid())

    def test_date_invalid(self):
        # a date in the past
        date = timezone.now() - timedelta(days=2)
        data = {
            "title": "event title",
            "description": "event description",
            "date": date.strftime("%Y-%m-%d")
        }
        form = EventForm(data=data)
        self.assertEqual(form.errors["date"], [
                         "Event date cannot be in the past!"])
