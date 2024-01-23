from django.urls import path
from borrowings_app.views import (
    BorrowingListCreateView,
    BorrowingDetailView,
    borrowing_return_view,
)

app_name = "borrowings_app"

urlpatterns = [
    path("", BorrowingListCreateView.as_view(), name="borrowing-list"),
    path("<int:pk>/", BorrowingDetailView.as_view(), name="borrowing-detail"),
    path(
        "<int:pk>/return/",
        borrowing_return_view,
        name="borrowing-return",
    ),
]
