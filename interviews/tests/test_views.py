from model_mommy import mommy
from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse

from interviews.models import Employee, EmployeeAvailability
from interviews.views import EmployeeAvailabilityViewSet, EmployeeViewSet, AvailableTimeSlotsListViewSet


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

    # def test_retrieve(self):
    #     employee = self.employee_model
    #     view = EmployeeAvailabilityViewSet()
    #     view.kwargs = {'employee_pk': employee.id}
    #     queryset = view.create(
    #
    #     )
    #     self.assertEquals([i for i in queryset], [employee])


class TestAvailableTimeSlotsListViewSet(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.employee_model = mommy.make(Employee)
        self.employee_availability_model = mommy.make(EmployeeAvailability, employee_id=self.employee_model.id,
                                                      _quantity=5)

    # def test_get_query_set(self):
    #     employee = self.employee_model
    #     employee_availability = self.employee_availability_model
    #     view = AvailableTimeSlotsListViewSet()
    #     view.kwargs = {'employee_pk': employee.id}
    #     # view.query_params['candidate_id'] = 5
    #
    #     self.client.post('/api/timeslots/?candidate_id=5&employee_id=5', format='json')
    #
    #     view.initialize_request(request=self.client)
    #     # view.request.query_params['employee_id'] = 5
    #     queryset = view.get_queryset()
    #     self.assertEquals([i for i in queryset], [i for i in employee_availability])
