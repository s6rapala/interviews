from datetime import datetime

from rest_framework import viewsets

from interviews import utils
from interviews.response import Http400, Http422
from interviews.serializers import *


class AvailableTimeSlotsListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AvailableTimeSlotsListSerializer

    def get_queryset(self):
        # this func gets called twice (based on django debug report)
        # google tells it's because of permission evaluation inside BrowseableAPI
        candidate_id, employee_ids, start_date, end_date = self.validate_input()
        queryset_candidate_timeslots = CandidateAvailability.objects \
            .filter(candidate_id=candidate_id, start_date__gte=start_date, end_date__lte=end_date) \
            .values('candidate_id', 'start_date', 'end_date')
        queryset_employee_timeslots = EmployeeAvailability.objects \
            .filter(employee_id__in=employee_ids, start_date__gte=start_date, end_date__lte=end_date) \
            .values('employee_id', 'start_date', 'end_date')

        possible_dates = utils.intersection(queryset_candidate_timeslots, queryset_employee_timeslots)

        # return AvailableTimeSlotsListSerializer(possible_dates, many=True).data
        return possible_dates

    def validate_input(self) -> (int, list):
        """
        ensure that all arguments passed are of type int
        """
        candidate_id, employee_ids = self.parse_employee_and_candidate_ids()
        end_date, start_date = self.parse_start_and_end_date()
        # TODO AttributeError
        return candidate_id, employee_ids, start_date, end_date

    def parse_start_and_end_date(self):
        """
        get start and end dates from the query. if they are not supplied,
        replace them with monday and friday of the next week correspondingly
        """
        if self.has_both_dates():
            try:
                start_date = datetime.strptime(self.request.query_params['start_date'], '%d%m%Y')
                end_date = datetime.strptime(self.request.query_params['end_date'], '%d%m%Y')
            except ValueError:
                raise Http422()
        else:
            start_date, end_date = utils.start_and_end_date_of_next_week()
        return end_date, start_date

    def parse_employee_and_candidate_ids(self):
        if self.is_missing_employee_or_candidate_id():
            raise Http400()
        try:
            candidate_id = int(self.request.query_params['candidate_id'][0])
            employee_ids = [int(i) for i in self.request.query_params['employee_id'].split(',')]
        except ValueError:
            raise Http422()
        return candidate_id, employee_ids

    def has_both_dates(self):
        return 'start_date' in self.request.query_params and 'end_date' in self.request.query_params

    def is_missing_employee_or_candidate_id(self):
        return 'employee_id' not in self.request.query_params or 'candidate_id' not in self.request.query_params
