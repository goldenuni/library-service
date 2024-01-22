from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from borrowings_app.models import Borrowing
from borrowings_app.serializers import (
    BorrowingReadSerializer,
    BorrowingCreateSerializer,
)


class BorrowingListCreateView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BorrowingCreateSerializer

        return BorrowingReadSerializer


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingReadSerializer
    permission_classes = [
        IsAuthenticated,
    ]
