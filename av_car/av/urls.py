from rest_framework.routers import DefaultRouter

from .views import *
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'car', CarViewSet, 'cars')

# urlpatterns = router.urls
urlpatterns = [
    path('', car_list, name='mymodel-list'),
    path('', include(router.urls)),
]
