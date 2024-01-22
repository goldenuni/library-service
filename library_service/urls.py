from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("books_app.urls")),
    path("api/users/", include("users.urls",)),
    path("api/borrowings/", include("borrowings_app.urls"))
]
