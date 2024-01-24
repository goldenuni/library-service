import datetime

from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from borrowings_app.models import Borrowing
from borrowings_app.serializers import (
    BorrowingReadSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)
from borrowings_app.tasks import send_notification_task
from telegram_helper import TelegramHelper


class BorrowingListCreateView(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BorrowingCreateSerializer

        return BorrowingReadSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Borrowing.objects.all()

        is_active = self.request.query_params.get("is_active", "").lower()

        if user.is_staff:
            user_id = self.request.query_params.get("user_id")

            if user_id:
                queryset = queryset.filter(user_id=int(user_id))
        else:
            queryset = queryset.filter(user_id=user.id)

        if is_active == "true":
            queryset = queryset.filter(is_active=True)
        elif is_active == "false":
            queryset = queryset.filter(is_active=False)

        return queryset

    def perform_create(self, serializer):
        borrowing = serializer.save()

        telegram_helper = TelegramHelper(
            token=settings.TELEGRAM_BOT_TOKEN, chat_id=settings.TELEGRAM_CHAT_ID
        )
        message = (
            f"New Borrowing Created:\n"
            f"User: {borrowing.user.username}\n"
            f"Book: {borrowing.book.title}"
        )
        telegram_helper.send_message(message)


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingReadSerializer
    permission_classes = [
        IsAuthenticated,
    ]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def borrowing_return_view(request, pk: int):
    try:
        instance = Borrowing.objects.get(pk=pk)
    except Borrowing.DoesNotExist:
        return Response(
            {
                "Error": "Not Found",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "POST":
        if instance.is_active:
            updated_data = {
                "is_active": False,
                "actual_return_date": datetime.date.today(),
            }

            serializer = BorrowingReturnSerializer(
                instance,
                data=updated_data,
                partial=True,
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"Error": "You cannot return borrowing twice"},
                status=status.HTTP_403_FORBIDDEN,
            )
