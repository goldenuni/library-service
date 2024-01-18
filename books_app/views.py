from rest_framework import viewsets

from books_app.models import Book
from books_app.permissions import ReadOnlyOrAdminPermission
from books_app.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (ReadOnlyOrAdminPermission,)
