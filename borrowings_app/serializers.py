from rest_framework import serializers

from books_app.serializers import BookSerializer
from borrowings_app.models import Borrowing


class BorrowingReadSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Borrowing
        fields = "__all__"
