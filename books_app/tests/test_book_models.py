from django.test import TestCase
from books_app.models import Book


class BookModelTest(TestCase):

    def setUp(self):
      self.book = Book.objects.create(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            cover=Book.SOFT,
            inventory=50,
            daily_fee=7.99
        )

    def test_str_method(self):
        self.assertEqual(str(self.book), "To Kill a Mockingbird")
