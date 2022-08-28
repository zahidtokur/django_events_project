from django.test import TestCase

from account.forms import RegisterForm


class RegisterFormTestCase(TestCase):
    def test_valid_form(self):
        data = {
            "email": "example@gmail.com",
            "password1": "examplepassword",
            "password2": "examplepassword"
        }
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.is_active)

    def test_with_no_email(self):
        data = {
            "email": "example",
            "password1": "examplepassword",
            "password2": "examplepassword"
        }
        form = RegisterForm(data=data)
        self.assertEqual(form.errors["email"], [
                         "Enter a valid email address."])

    def test_passwords_dont_match(self):
        data = {
            "email": "example@gmail.com",
            "password1": "examplepassword",
            "password2": "nonmatchingpassword"
        }
        form = RegisterForm(data=data)
        self.assertEqual(form.errors['password2'], [
                         "The two password fields didn’t match."])
