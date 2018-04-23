from rest_framework import viewsets

from interviews.response import Http400, Http422
from interviews.serializers import *
from interviews.utils import intersection


class AvailableTimeSlotsListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AvailableTimeSlotsListSerializer

    def get_queryset(self):
        # this func gets called twice (based on django debug report)
        # google tells it's because of permission evaluation inside BrowseableAPI
        candidate_id, employee_ids = self.validate_input()
        queryset_candidate_timeslots = CandidateAvailability.objects \
            .filter(candidate_id=candidate_id) \
            .values('candidate_id', 'start_date', 'end_date')
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
