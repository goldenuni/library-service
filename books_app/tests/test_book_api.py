from decimal import Decimal, ROUND_DOWN
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books_app.models import Book
from books_app.serializers import BookSerializer

BOOK_URL = reverse("books_app:book-list")


def detail_url(book_id: int):
    return reverse("books_app:book-detail", args=[book_id])


def sample_book(**params):
    defaults = {
        "title": "test-book",
        "author": "test-author",
        "cover": Book.HARD,
        "inventory": 10,
        "daily_fee": 9.99,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


class UnauthenticatedBookApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_Book(self):
        sample_book()

        res = self.client.get(BOOK_URL)

        facilities = Book.objects.all()
        serializer = BookSerializer(facilities, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_unauth_cannot_create_book(self):
        defaults = {
            "title": "test book",
            "author": "test author",
            "cover": Book.SOFT,
            "inventory": 30,
            "daily_fee": 15.99,
        }

        res = self.client.post(BOOK_URL, defaults)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_Book(self):
        sample_book()

        res = self.client.get(BOOK_URL)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_forbidden(self):
        defaults = {
            "title": "test book",
            "author": "test author",
            "cover": Book.SOFT,
            "inventory": 30,
            "daily_fee": 15.99,
        }

        res = self.client.post(BOOK_URL, defaults)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com", "test12345", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": Book.SOFT,
            "inventory": 30,
            "daily_fee": 15.99,
        }

        res = self.client.post(BOOK_URL, payload)
        book = Book.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        payload["daily_fee"] = Decimal(15.99).quantize(
            Decimal("0.00"), rounding=ROUND_DOWN
        )
        for key in payload:
            self.assertEqual(payload[key], getattr(book, key))

    def test_update_book(self):
        book = sample_book()
        payload = {
            "title": "updated-book",
        }
        url = detail_url(book.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        book = sample_book()
        url = detail_url(book.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
