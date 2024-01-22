from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from borrowings_app.models import Borrowing
from borrowings_app.serializers import BorrowingReadSerializer


class BorrowingListView(generics.ListAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingReadSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingReadSerializer
    permission_classes = [
        IsAuthenticated,
    ]
