from django.test import TestCase
from .models import *
from .forms import *
import datetime


class TestProfileModel(TestCase):
    def create_profile(self):
        user = User.objects.create_user("user", "user1@example.com", "example")
        user2 = User.objects.create_user("friend", "friend@example.com", "friend")
        friend = Profile.objects.create(user=user2, date_of_birth=datetime.datetime(1999, 3, 3))
        profile = Profile.objects.create(user=user, date_of_birth=datetime.datetime(1997, 3, 3))
        profile.friends.add(friend)
        return profile

    def test_str_method(self):
        profile = self.create_profile()
        self.assertEqual("Profil użytkownika user.", profile.str())

    def test__str__(self):
        profile = self.create_profile()
        self.assertEqual(str(profile), "user")

    def test_date_birth(self):
        profile = self.create_profile()
        self.assertEqual(profile.date_of_birth, datetime.datetime(1997, 3, 3))

    def test_friend_exist(self):
        profile = self.create_profile()
        is_friend = False
        for f in profile.friends.all():
            if f.user.username == "friend":
                is_friend = True
        self.assertTrue(is_friend)
        # sprint 9

    def test_rate_default(self):
        profile = self.create_profile()
        self.assertEqual(profile.rate, 0)

    def test_rate_set(self):
        profile = self.create_profile()
        profile.rate = 3
        self.assertEqual(profile.rate, 3)


class FormsTests(TestCase):
    def test_login_page_valid(self):
        data = {'username': 'username', 'password': 'password'}
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_login_page_not_valid(self):
        data = {'username': 'username', 'password': ''}
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())

