from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from books_app.models import Book
from borrowings_app.models import Borrowing


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassYo12345",
            first_name="Johny",
            last_name="Dog",
        )

        self.book = Book.objects.create(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            cover=Book.SOFT,
            inventory=50,
            daily_fee=7.99,
        )

        self.str_output = "Johny Dog borrowed To Kill a Mockingbird"

    def test_validate_borrowing(self):
        Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            book=self.book,
            user=self.user,
            is_active=True,
        )

        self.assertEqual(1, Borrowing.objects.count())

    def test_invalid_expected_return_date(self):
        """
        Test case where expected_return_date is before borrow_date
        """
        borrowing = Borrowing(
            borrow_date=date.today(),
            expected_return_date=date.today() - timedelta(days=1),
            book=self.book,
            user=self.user,
            is_active=True,
        )

        with self.assertRaises(ValidationError):
            borrowing.full_clean()

    def test_invalid_actual_return_date(self):
        """
        Test case where actual_return_date is before borrow_date
        """
        borrowing = Borrowing(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=date.today() - timedelta(days=1),
            book=self.book,
            user=self.user,
            is_active=True,
        )

        with self.assertRaises(ValidationError):
            borrowing.full_clean()

    def test_invalid_active_with_actual_return_date(self):
        """
        Test case where is_active is True, but actual_return_date is provided"
        """
        borrowing = Borrowing(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=date.today(),
            book=self.book,
            user=self.user,
            is_active=True,
        )

        with self.assertRaises(ValidationError):
            borrowing.full_clean()

    def test_invalid_not_active_with_null_actual_return_date(self):
        """
        Test case where is_active is False, but actual_return_date is None
        """
        borrowing = Borrowing(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=None,
            book=self.book,
            user=self.user,
            is_active=False,
        )

        with self.assertRaises(ValidationError):
            borrowing.full_clean()

    def test_invalid_book_inventory_zero(self):
        """
        Test case where book inventory is zero
        """
        self.book.inventory = 0
        self.book.save()

        borrowing = Borrowing(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            book=self.book,
            user=self.user,
            is_active=True,
        )

        with self.assertRaises(ValidationError):
            borrowing.full_clean()

    def test_str_method(self):
        borrowing = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            book=self.book,
            user=self.user,
            is_active=True,
        )

        self.assertEqual(str(borrowing), self.str_output)
