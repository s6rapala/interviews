# Create your views here.
from django.http import Http404, HttpResponseGone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from interviews.models import EmployeeAvailability, Employee
from interviews.response import Http422, Http400
from interviews.serializers import EmployeeAvailabilityListSerializer, EmployeeSerializerDetail, EmployeeListSerializer, \
    AvailableTimeSlotsListSerializer
from .utils import intersection


class EmployeeAvailabilityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employee availability to be viewed or edited
    """
    # queryset = EmployeeAvailability.objects.all()
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


class AvailableTimeSlotsListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AvailableTimeSlotsListSerializer

    def get_queryset(self):
        # this func gets called twice (based on django debug report)
        # google tells it's because of permission evaluation inside BrowseableAPI
        candidate_id, employee_ids = self.validate_input()
        queryset_candidate_timeslots = EmployeeAvailability.objects \
            .filter(employee_id=candidate_id) \
            .values('employee_id', 'start_date', 'end_date')
        queryset_employee_timeslots = EmployeeAvailability.objects \
            .filter(employee_id__in=employee_ids) \
            .values('employee_id', 'start_date', 'end_date')
        possible_dates = intersection(queryset_candidate_timeslots, queryset_employee_timeslots)

        # return AvailableTimeSlotsListSerializer(possible_dates, many=True).data
        return possible_dates

    def validate_input(self) -> (int, list):
        try:
            candidate_id = int(self.request.query_params['candidate_id'][0])
            employee_ids = [int(i) for i in self.request.query_params['employee_id'].split(',')]
        except KeyError:
            raise Http400()
        except ValueError:
            raise Http422()

        # TODO AttributeError
        return candidate_id, employee_ids
