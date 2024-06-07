from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import Car
from .serializers import CarSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    permission_classes = [
      permissions.AllowAny
    ]
    serializer_class = CarSerializer


def car_list(request):
    car = Car.objects.all()
    return render(request, 'av/index.html', {'car': car})
