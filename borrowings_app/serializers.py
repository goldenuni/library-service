from rest_framework import serializers

from books_app.serializers import BookSerializer
from borrowings_app.models import Borrowing


class BorrowingReadSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowingCreateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(BorrowingCreateSerializer, self).validate(attrs)
        Borrowing.validate_borrowing(
            borrow_date=data.get("borrow_date"),
            expected_return_date=data.get("expected_return_date"),
            book=data.get("book"),
            error_to_raise=serializers.ValidationError,
            is_active=data.get("is_active"),
            actual_return_date=data.get("actual_return_date"),
        )
        return data

    def save(self):
        book = self.validated_data["book"]

        if book.inventory > 0:
            book.inventory -= 1
            book.save()
        else:
            raise serializers.ValidationError(
                "Book inventory is 0, you cannot take this book"
            )

        return super().create(self.validated_data)

    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowingReturnSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    def save(self):
        instance = super().update(self.instance, self.validated_data)

        book = instance.book
        book.inventory += 1
        book.save()

        return instance

    class Meta:
        model = Borrowing
        fields = "__all__"
