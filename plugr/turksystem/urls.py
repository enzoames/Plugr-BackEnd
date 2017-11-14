from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import * 

router = DefaultRouter()

# router.register(r'user/(?P<slug>\w+)', TurkUserViewSet, base_name='turkuser')
router.register(r'user', TurkUserViewSet, base_name='turkuser')
router.register(r'login', LoginTurkUserViewSet, base_name='loginturkuser')
router.register(r'load', LoadTurkUserViewSet, base_name='loadturkuser')
router.register(r'logout', LogoutTurkUserViewSet, base_name='logoutturkuser')
router.register(r'register', RegisterViewSet, base_name='registeruser')

urlpatterns = [
    url(r'^', include(router.urls)),
]