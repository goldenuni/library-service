from django.urls import path
from borrowings_app.views import BorrowingListCreateView, BorrowingDetailView


app_name = "borrowings_app"

urlpatterns = [
    path("", BorrowingListCreateView.as_view(), name="borrowing-list"),
    path(
        "<int:pk>/", BorrowingDetailView.as_view(), name="borrowing-detail"
    ),
]
