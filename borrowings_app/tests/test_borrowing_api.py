from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from borrowings_app.models import Borrowing
from books_app.models import Book
from borrowings_app.serializers import BorrowingReadSerializer

BORROWINGS_LIST_URL = reverse("borrowings_app:borrowing-list")


def detail_url(borrowing_id: int):
    return reverse("borrowings_app:borrowing-detail", args=[borrowing_id])


def return_url(borrowing_id: int):
    return reverse("borrowings_app:borrowing-return", args=[borrowing_id])


def sample_book(**params):
    defaults = {
        "title": "Lorem ipsum",
        "author": "John Connor",
        "cover": Book.HARD,
        "inventory": 10,
        "daily_fee": 9.99,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


def sample_user(**params):
    defaults = {
        "email": "testovich@test.com",
        "password": "MegaSecretHardPass1204",
    }
    defaults.update(params)

    return get_user_model().objects.create_user(**defaults)


class UnauthenticatedBorrowingTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_list_endpoint(self):
        res = self.client.get(BORROWINGS_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_detail_endpoint(self):
        url = detail_url(1)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_return_endpoint(self):
        url = reverse("borrowings_app:borrowing-return", args=[1])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345",
        )
        self.client.force_authenticate(self.user)

    def test_create_borrowing(self):
        """
        Test creating a new borrowing,
        checking if book inventory decreasing by one.
        """
        book = sample_book()
        data = {
            "borrow_date": date.today(),
            "expected_return_date": date.today(),
            "book": book.id,
            "user": self.user.id,
            "is_active": True,
        }

        res = self.client.post(BORROWINGS_LIST_URL, data)

        book.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 1)
        self.assertEqual(book.inventory, 9)

    def test_create_forbidden_when_book_inventory_zero(self):
        book = sample_book(inventory=0)
        data = {
            "borrow_date": date.today(),
            "expected_return_date": date.today(),
            "book": book.id,
            "user": self.user.id,
            "is_active": True,
        }

        res = self.client.post(BORROWINGS_LIST_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_borrowings(self):
        book = sample_book()

        Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            book=book,
            user=self.user,
            is_active=True,
        )

        borrowings = Borrowing.objects.all()
        serializer = BorrowingReadSerializer(borrowings, many=True)

        res = self.client.get(BORROWINGS_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_borrowing_detail(self):
        book = sample_book()

        Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            book=book,
            user=self.user,
            is_active=True,
        )

        borrowing = Borrowing.objects.get(pk=1)
        serializer = BorrowingReadSerializer(borrowing)

        url = detail_url(1)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_borrowing_return(self):
        book = sample_book(inventory=1)

        Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            book=book,
            user=self.user,
            is_active=True,
        )

        url = return_url(1)
        res = self.client.post(url)

        borrowing = Borrowing.objects.get(pk=1)
        serializer = BorrowingReadSerializer(borrowing)
        book.refresh_from_db()

        self.assertEqual(book.inventory, 2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_borrowing_cannot_return_twice(self):
        book = sample_book()

        Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=date.today(),
            book=book,
            user=self.user,
            is_active=False,
        )

        url = return_url(1)
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_is_active(self):
        book1 = sample_book()
        book2 = sample_book(title="Param Baram")

        Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=date.today(),
            book=book1,
            user=self.user,
            is_active=False,
        )

        Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=None,
            book=book2,
            user=self.user,
            is_active=True,
        )

        url = f"{BORROWINGS_LIST_URL}?is_active=true"
        res = self.client.get(url)

        data = Borrowing.objects.filter(is_active=True)
        serializer = BorrowingReadSerializer(data, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AdminBorrowingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com", "test12345", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_admin_can_filter_by_user_id(self):
        book = sample_book()
        user = sample_user()

        Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=None,
            book=book,
            user=user,
            is_active=True,
        )

        Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=None,
            book=book,
            user=self.user,
            is_active=True,
        )

        url = f"{BORROWINGS_LIST_URL}?user_id={user.id}"

        res = self.client.get(url)
        data = Borrowing.objects.filter(user_id=user.id)

        serializer = BorrowingReadSerializer(data, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
