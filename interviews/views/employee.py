import django_filters
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.response import Response

from interviews.serializers import *


class EmployeeAvailabilityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Employee availability to be viewed or edited
    """
    serializer_class = EmployeeAvailabilityListSerializer

    def get_queryset(self):
        return EmployeeAvailability.objects.filter(employee=self.kwargs['employee_pk'])

    def perform_create(self, serializer):
        """
        Notes:
        Get employee_id from the request so we can insert it into a database
        Don't have to worry about SQL injections because we have regex \d+ in urls.py
        TODO Might be a better idea to override inside serializer
        TODO Given an non-existing employee_id will give FK constraint violation

        """
        serializer.save(employee_id=self.kwargs['employee_pk'])


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Employees to be viewed or edited
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ('name',)  # only exact match (but can be a regex search with $)

    def retrieve(self, request, pk=None, **kwargs):
        """
        Override retrieve method so that we can display timeslots for a specific employee
        (instead of basic information of an employee without timeslots belonging to them)

        Not required, but the API looks more useful this way
        """
        queryset = Employee.objects.all()
        # TODO because there is a nested Serializer we query database with 2 separate queries
        # need to change these 2 queries into a single one with INNER JOIN
        user = get_object_or_404(queryset, pk=pk)
        serializer = EmployeeSerializerDetail(user)
        return Response(serializer.data)
