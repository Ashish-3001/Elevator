from rest_framework import viewsets
from .models import Elevator, Request
from .serializers import ElevatorSerializer, RequestSerializer

class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer