# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.response import Response

from interviews.models import EmployeeAvailability, Employee
from interviews.serializers import EmployeeAvailabilitySerializer, EmployeeSerializerDetail, EmployeeSerializerList


class EmployeeAvailabilityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employee availability to be viewed or edited
    """
    # queryset = EmployeeAvailability.objects.all()
    serializer_class = EmployeeAvailabilitySerializer

    def get_queryset(self):
        return EmployeeAvailability.objects.filter(employee=self.kwargs['employee_pk'])


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Employees to be viewed or edited
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializerList

    def retrieve(self, request, pk=None):
        """
        Override retrieve method so that we can display timeslots for a specific employee
        (instead of just information of employee without timeslots belonging to them)
        """
        queryset = Employee.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = EmployeeSerializerDetail(user)
        return Response(serializer.data)
