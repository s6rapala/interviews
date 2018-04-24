from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIClient

from interviews.models import Employee


class TestTimeslots(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee = mommy.make(Employee)

    def test_get_correct_request_should_give_200(self):
        payload = {'candidate_id': self.employee.id, 'employee_id': self.employee.id}
        response = self.client.get(reverse('timeslots-list'), payload)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_incorrect_type_request_should_fail(self):
        payload = {'candidate_id': self.employee.id, 'employee_id': "string instead of int"}
        response = self.client.get(reverse('timeslots-list'), payload)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_missing_args_request_should_fail(self):
        payload = {'candidate_id': self.employee.id}
        response = self.client.get(reverse('timeslots-list'), payload)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_str(self):
    #     response = self.client.get('/api/employees/1')
    #     # response = view
    #
    #     # print(response.__dict__)
    #     # print(response.status_code)
    #     self.assertTrue(response.status_code == status.HTTP_301_MOVED_PERMANENTLY)
    #
    # def test_post_user(self):
    #     url = reverse('employee-list')
    #     # print(reverse('employee-detail'))
    #     response = self.client.post(url, {'name': 'user1'}, format='json')
    #     self.assertEquals(response.status_code, status.HTTP_201_CREATED)
    #
    # def test_get_timeslots(self):
    #     url = reverse('timeslots-list')
    #     print(url)
    #     # print(reverse('employee-detail'))
    #     response = self.client.get(url + '1')
    #     print(response.__dict__)
    #     self.assertEquals(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
