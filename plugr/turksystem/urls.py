from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import * 

router = DefaultRouter()

router.register(r'user/(?P<slug>\w+)', TurkUserViewSet, base_name='turkuser')
router.register(r'user', TurkUserViewSet, base_name='turkuser')
router.register(r'login', LoginTurkUserViewSet, base_name='loginturkuser')
router.register(r'load', LoadTurkUserViewSet, base_name='loadturkuser')
router.register(r'logout', LogoutTurkUserViewSet, base_name='logoutturkuser')
router.register(r'register', RegisterViewSet, base_name='registeruser')
router.register(r'sysdemand', SysDemandViewSet, base_name='post_sysdemand')
router.register(r'deposite',DepositeViewSet,base_name='deposite')
#dont touch the order of these urls
router.register(r'bid/email', BidByEmailViewSet, base_name ='emailbid') #bids by email, for either dev or client
router.register(r'bid', BidViewSet, base_name ='postbid') # get all bids, post a bid
router.register(r'bid/sd/(?P<sd>\d+)', BidBySDIDViewSet, base_name ='sdbid') #bid by system demand
#router.register(r'bid/(?P<bid_sd>\w+)', BidByEmailViewSet, base_name ='emailbid') #bids by email, for either dev or client


# r'^(index|weblog)/$' 

urlpatterns = [
    url(r'^', include(router.urls)),
]
