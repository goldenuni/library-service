from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from books_app.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(
        null=True,
        blank=True,
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"{self.user.first_name} {self.user.last_name} "
            f"borrowed {self.book.title}"
        )

    @staticmethod
    def validate_borrowing(
        borrow_date: date,
        expected_return_date: date,
        book: Book,
        error_to_raise: Exception,
        is_active: bool = True,
        actual_return_date: date = None,
    ):
        if book.inventory > 0:
            if borrow_date <= expected_return_date:
                if actual_return_date and is_active:
                    raise error_to_raise(
                            {
                                "Is active ERROR": "If status is_active is True, "
                                                   "therefore actual_return_date "
                                                   "must be None or vice verse",
                            }
                    )
                elif actual_return_date:
                    if actual_return_date < borrow_date:
                        raise error_to_raise(
                            {
                                "Actual return date ERROR":
                                    "Actual return date must be "
                                    "greater or equal to borrow_date",
                            }
                        )
                elif actual_return_date is None and not is_active:
                    raise error_to_raise(
                        {
                            "Is active ERROR": "Actual return date cannot be None "
                                               "or is_active must be True"
                        }
                    )
            else:
                raise error_to_raise(
                    {
                        "Expected return date ERROR":
                            "Expected return date must be "
                            "greater or equal to borrow_date"
                    }
                )
        else:
            raise error_to_raise(
                {
                    "Book inventory ERROR":
                        "Book inventory is 0, you cannot take this book"
                }
            )

    def clean(self):
        Borrowing.validate_borrowing(
            self.borrow_date,
            self.expected_return_date,
            self.book,
            ValidationError,
            self.is_active,
            self.actual_return_date,
        )
