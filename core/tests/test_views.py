from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from datetime import timedelta

from core.models import Event
from account.models import User


class EventViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_email = "test@email.com"
        self.user_password = "testpassword"
        self.user = self.create_user(
            self.user_email, self.user_password)
        self.event = self.create_event(
            user=self.user, title="Event title", description="Event description")

    def create_event(self, user, title, description):
        date = timezone.now() + timedelta(days=1)
        return Event.objects.create(
            created_by=user, title=title,
            description=description, date=date.date())

    def create_user(self, email, password):
        return User.objects.create_user(email, password)

    def login_user(self, email, password):
        response = self.client.post(reverse('login'), data={
            "username": email,
            "password": password})
        return response.status_code

    def test_event_list_view_GET(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/event_list.html')

    def test_created_event_list_view_GET(self):
        response = self.client.get(reverse('created_list'))
        # login required view, since there is no authenticated user, redirects to login page
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'core/event_list.html')

        self.login_user(self.user_email, self.user_password)
        # logged in user can access the view
        response = self.client.get(reverse('created_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/event_list.html')
        self.assertIn(self.event, response.context_data['object_list'])

    def test_joined_event_list_view_GET(self):
        response = self.client.get(reverse('created_list'))
        # login required view, since there is no authenticated user, redirects to login page
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'core/event_list.html')

        self.login_user(self.user_email, self.user_password)
        # add user to guests
        self.event.guests.add(self.user)
        # logged in user can access the view
        response = self.client.get(reverse('created_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/event_list.html')
        self.assertIn(self.event, response.context_data['object_list'])

    def test_create_event_view_GET(self):
        response = self.client.get(reverse('create'))
        # login required view, since there is no authenticated user, redirects to login page
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'core/event_create.html')

        self.login_user(self.user_email, self.user_password)
        # logged in user can access the view
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/event_create.html')

    def test_create_event_view_POST(self):
        self.login_user(self.user_email, self.user_password)
        event_date = timezone.now() + timedelta(days=3)
        event_title = "Test Event Title 2"
        data = {
            "title": event_title,
            "description": "description",
            "date": event_date.strftime("%Y-%m-%d")
        }
        response = self.client.post(reverse('create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(
            created_by=self.user, title=event_title).exists())

    def test_update_event_view_GET(self):
        response = self.client.get(
            reverse('update', kwargs={"pk": self.event.pk}))
        # login required view, since there is no authenticated user, redirects to login page
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'core/event_update.html')

        self.login_user(self.user_email, self.user_password)
        # logged in user can access the view
        response = self.client.get(
            reverse('update', kwargs={"pk": self.event.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/event_update.html')

        # create and login a new user that isn't the creator of the event
        new_user_email = "test2@email.com"
        new_user_password = "testpassword"
        new_user = self.create_user(new_user_email, new_user_password)
        self.login_user(new_user_email, new_user_password)

        # creator of the event is not the new user and can't access the view
        response = self.client.get(
            reverse('update', kwargs={"pk": self.event.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'core/event_update.html')

    def test_update_event_view_POST(self):
        self.login_user(self.user_email, self.user_password)
        event_title = "Updated event title"
        data = {
            "title": event_title,
            "description": self.event.description,
            "date": self.event.date
        }

        self.assertFalse(Event.objects.filter(
            created_by=self.user, title=event_title).exists())
        response = self.client.post(
            reverse('update', kwargs={"pk": self.event.pk}), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(
            created_by=self.user, title=event_title).exists())

    # def test_delete_event_view(self):

    # def test_join_event_view(self):

    # def test_unjoin_event_view(self):
