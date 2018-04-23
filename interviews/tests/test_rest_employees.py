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
        self.assertTrue(response.status_code == status.HTTP_200_OK)

    def test_get_incorrect_type_request_should_fail(self):
        payload = {'candidate_id': self.employee.id, 'employee_id': "string instead of int"}
        response = self.client.get(reverse('timeslots-list'), payload)
        self.assertTrue(response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_get_missing_args_request_should_fail(self):
        payload = {'candidate_id': self.employee.id}
        response = self.client.get(reverse('timeslots-list'), payload)
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
