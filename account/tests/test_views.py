from django.test import TestCase, Client
from django.urls import reverse
from account.models import User


class AccountViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def create_user(self, email, password):
        user = User.objects.create_user(email=email, password=password)
        return user

    def test_signup_view_GET(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_signup_view_POST(self):
        user_email = "test@email.com"
        self.assertEqual(User.objects.filter(email=user_email).count(), 0)

        data = {
            "email": user_email,
            "password1": "matchingpassword",
            "password2": "matchingpassword"
        }
        response = self.client.post(reverse('register'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.filter(email=user_email).count(), 1)

    def test_login_view_GET(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_view_POST(self):
        user_email = "test@email.com"
        user_password = "test_password"
        self.create_user(user_email, user_password)

        data = {
            "username": user_email,
            "password": user_password
        }

        response = self.client.post(reverse('login'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
