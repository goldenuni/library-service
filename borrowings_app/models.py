from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from books_app.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(
        validators=[MinValueValidator(borrow_date)]
    )
    actual_return_date = models.DateField(
        null=True, blank=True, validators=[MinValueValidator(borrow_date)]
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.user.first_name} {self.user.last_name} borrowed {self.book.title}"
        )
