from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="testovich@test.com",
            password="UltraSecretPassword304!",
            first_name="John",
            last_name="Lennon",
        )

    def test_str_method(self):
        self.assertEqual(str(self.user), "John Lennon (testovich@test.com)")
