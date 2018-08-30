from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import path
from geocode_excel.views import AddressApiViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"address", AddressApiViewSet)

urlpatterns = [url(r"^", include(router.urls))] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
