from datetime import datetime

from rest_framework import viewsets

from interviews import utils
from interviews.response import Http400
from interviews.serializers import *


class AvailableTimeSlotsListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AvailableTimeSlotsListSerializer

    def get_queryset(self):
        # this func gets called twice (based on django debug report)
        # google tells it's because of permission evaluation inside BrowseableAPI
        data = TimeSlotsSerializer(data=self.request.query_params)
        if not data.is_valid():
            raise Http400()  # don't want to give away data.errors
        candidate_id, employee_ids, start_date, end_date = self.unpack_schedule_dict(**data.validated_data)

        queryset_candidate_timeslots = CandidateAvailability.objects \
            .filter(candidate_id=candidate_id, start_date__gte=start_date, end_date__lte=end_date) \
            .values('candidate_id', 'start_date', 'end_date')
        queryset_employee_timeslots = EmployeeAvailability.objects \
            .filter(employee_id__in=employee_ids, start_date__gte=start_date, end_date__lte=end_date) \
            .values('employee_id', 'start_date', 'end_date')

        possible_dates = utils.intersection(queryset_candidate_timeslots, queryset_employee_timeslots)
        return possible_dates

    @staticmethod
    def unpack_schedule_dict(candidate_id, employee_id, start_date=datetime.now(), end_date=datetime.now()):
        return candidate_id, employee_id, start_date, end_date
