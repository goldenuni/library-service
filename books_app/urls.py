from rest_framework import routers

from books_app.views import BookViewSet


app_name = "books_app"

router = routers.DefaultRouter()
router.register("books", BookViewSet)


urlpatterns = router.urls
