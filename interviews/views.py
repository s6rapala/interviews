from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from api.serializers import EmployeeAvailabilitySerializer
from interviews.models import EmployeeAvailability


class EmployeeAvailabilityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = EmployeeAvailability.objects.all()
    serializer_class = EmployeeAvailabilitySerializer
