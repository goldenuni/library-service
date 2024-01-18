from django.db import models


class Book(models.Model):
    HARD = "HARD"
    SOFT = "SOFT"

    COVER_CHOICES = [
        (HARD, "Hardcover"),
        (SOFT, "Softcover"),
    ]

    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
