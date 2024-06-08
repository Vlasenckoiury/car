from rest_framework.routers import DefaultRouter

from .views import *
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'car', CarViewSet, 'car')

# urlpatterns = router.urls
urlpatterns = [
    path('', views.home),
    path('cars', views.car_list, name="cars"),
    path('', include(router.urls)),
]
