from rest_framework import viewsets

from interviews import utils
from interviews.serializers import *


class AvailableTimeSlotsListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AvailableTimeSlotsListSerializer

    def get_queryset(self):
        # these SQL queries get called twice (based on django debug report)
        # google tells it's because of permission evaluation inside BrowseableAPI
        data = TimeSlotsSerializerInput(data=self.request.query_params)
        data.is_valid(raise_exception=True)

        queryset_candidate_timeslots = CandidateAvailability.objects \
            .filter(candidate_id=data.validated_data['candidate_id'],
                    start_date__gte=data.validated_data['start_date'],
                    end_date__lte=data.validated_data['end_date']) \
            .values('candidate_id', 'start_date', 'end_date')
        queryset_employee_timeslots = EmployeeAvailability.objects \
            .filter(employee_id__in=data.validated_data['employee_id'],
                    start_date__gte=data.validated_data['start_date'],
                    end_date__lte=data.validated_data['end_date']) \
            .values('employee_id', 'start_date', 'end_date')

        # technically you can do intersection in the database, but computationally I would rather avoid it
        possible_dates = utils.intersection(queryset_candidate_timeslots, queryset_employee_timeslots)
        return possible_dates
