from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import * 

router = DefaultRouter()

router.register(r'gallery/(?P<slug>\w+)', PhotoByGalleryViewSet, base_name='individual-gallery')
router.register(r'contactenzoames', ContactEnzoAmesViewSet, base_name='contactenzoames')
# router.register(r'gallery', PhotoByGalleryViewSet, base_name='individual-gallery')
router.register(r'photos', PhotologueViewset, base_name='photos')

urlpatterns = [
    url(r'^', include(router.urls)),
]