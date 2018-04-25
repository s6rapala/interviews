from django.test import RequestFactory
from django.test import TestCase
from model_mommy import mommy

from interviews.models import Employee, EmployeeAvailability, Candidate, CandidateAvailability
from interviews.views.candidate import CandidateAvailabilityViewSet
from interviews.views.employee import EmployeeAvailabilityViewSet


class TestEmployeeAvailabilityViewSet(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.employee_model = mommy.make(Employee)
        self.employee_availability_model = mommy.make(EmployeeAvailability, employee_id=self.employee_model.id,
                                                      _quantity=5)

    def test_get_query_set(self):
        employee = self.employee_model
        employee_availability = self.employee_availability_model
        view = EmployeeAvailabilityViewSet()
        view.kwargs = {'employee_pk': employee.id}
        queryset = view.get_queryset()
        self.assertEquals([i for i in queryset], [i for i in employee_availability])


class TestCandidateAvailabilityViewSet(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.candidate_model = mommy.make(Candidate)
        self.candidate_availability_model = mommy.make(CandidateAvailability, candidate_id=self.candidate_model.id,
                                                       _quantity=5)

    def test_get_query_set(self):
        candidate = self.candidate_model
        candidate_availability = self.candidate_availability_model
        view = CandidateAvailabilityViewSet()
        view.kwargs = {'candidate_pk': candidate.id}
        queryset = view.get_queryset()
        self.assertEquals([i for i in queryset], [i for i in candidate_availability])
