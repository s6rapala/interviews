from datetime import datetime, timedelta

import pytz
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from interviews.models import Employee, EmployeeAvailability, Candidate, CandidateAvailability


class TestTimeslots(TestCase):
    YEAR = 2018
    MONTH = 4
    DAY = 25

    def setUp(self):
        self.client = APIClient()
        self.employee = mommy.make(Employee)
        self.candidate = mommy.make(Candidate)

        # create a new employee who is available the whole day
        self.employee_availability = mommy.make(EmployeeAvailability,
                                                employee_id=self.employee.id,
                                                start_date=self.construct_date(hour=8, minute=00),
                                                end_date=self.construct_date(hour=17, minute=00))

    def construct_date(self, hour, minute, year=YEAR):
        return datetime(year, self.MONTH, self.DAY, hour, minute)

    @staticmethod
    def convert_str_to_date(response, interval_point: str) -> datetime:
        return datetime.strptime(response.data[0][interval_point], '%Y-%m-%dT%H:%M:%SZ')

    def test_get_correct_request_should_give_200(self):
        payload = {
            'candidate_id': self.candidate.id,
            'employee_id': self.employee.id
        }
        response = self.client.get(reverse('timeslots-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_incorrect_type_request_should_fail(self):
        payload = {
            'candidate_id': self.employee.id,
            'employee_id': "string instead of int"
        }
        response = self.client.get(reverse('timeslots-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_missing_args_employee_request_should_fail(self):
        payload = {
            'candidate_id': self.candidate.id
        }
        response = self.client.get(reverse('timeslots-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_missing_args_candidate_request_should_fail(self):
        payload = {
            'employee_id': self.employee.id
        }
        response = self.client.get(reverse('timeslots-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_with_no_dates_1_common_slot_should_return_1_record(self):
        candidate_start_date = self.construct_date(hour=10, minute=00)
        candidate_end_date = self.construct_date(hour=12, minute=00)
        mommy.make(CandidateAvailability,
                   candidate_id=self.candidate.id,
                   start_date=candidate_start_date,
                   end_date=candidate_end_date)
        payload = self.meeting_on_specific_day_between_two_people()
        response = self.client.get(reverse('timeslots-list'), payload, format='json')
        employee_id = response.data[0]['employee_id']
        start_date = self.convert_str_to_date(response, 'start_date')
        end_date = self.convert_str_to_date(response, 'end_date')

        self.assertEqual(employee_id, self.employee.id)
        self.assertEqual(start_date, candidate_start_date)
        self.assertEqual(end_date, candidate_end_date)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'employee_id')
        self.assertContains(response, 'start_date')
        self.assertContains(response, 'end_date')
        self.assertEqual(len(response.data), 1)

    def test_get_with_no_dates_2_common_slots_should_return_2_record(self):
        candidate_start_date = self.construct_date(hour=10, minute=00)
        candidate_end_date = self.construct_date(hour=12, minute=00)
        self.make_two_timeslots_for_a_candidate(candidate_end_date, candidate_start_date)
        payload = self.meeting_on_specific_day_between_two_people()
        response = self.client.get(reverse('timeslots-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'employee_id')
        self.assertContains(response, 'start_date')
        self.assertContains(response, 'end_date')
        self.assertEqual(len(response.data), 2)

    def test_get_with_no_dates_0_common_slots_should_return_0_record(self):
        candidate_start_date = self.construct_date(year=1900, hour=10, minute=00)
        candidate_end_date = self.construct_date(year=1900, hour=12, minute=00)
        self.make_two_timeslots_for_a_candidate(candidate_end_date, candidate_start_date)
        payload = self.meeting_on_specific_day_between_two_people()
        response = self.client.get(reverse('timeslots-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def meeting_on_specific_day_between_two_people(self):
        return {
            'candidate_id': self.candidate.id,
            'employee_id': self.employee.id,
            'start_date': self.construct_date(hour=0, minute=0),
            'end_date': self.construct_date(hour=23, minute=59)
        }

    def make_two_timeslots_for_a_candidate(self, candidate_end_date, candidate_start_date):
        for i in range(2):
            mommy.make(CandidateAvailability,
                       candidate_id=self.candidate.id,
                       start_date=candidate_start_date,
                       end_date=candidate_end_date + timedelta(seconds=i))  # dates must be different


class TestEmployeeViewSet(APITestCase):
    def setUp(self):
        self.employee = mommy.make(Employee)

    def test_retrieve_employee(self):
        url = reverse('employee-detail', kwargs={'pk': self.employee.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().name, self.employee.name)

    def test_list_employees(self):
        url = reverse('employee-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().name, self.employee.name)

    def test_create_employee(self):
        url = reverse('employee-list')
        employee_name = 'employee 1'
        data = {'name': employee_name}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
        self.assertEqual(Employee.objects.get(name=employee_name).name, employee_name)


class TestEmployeeAvailabilityViewSetAPI(APITestCase):
    def setUp(self):
        self.model = mommy.make(Employee)

    def test_create_employee(self):
        now = datetime.now(pytz.utc)
        future = now + timedelta(days=1)
        url = reverse('employee-timeslots-list', kwargs={'employee_pk': self.model.id})
        data = {'start_date': now, 'end_date': future}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmployeeAvailability.objects.count(), 1)
        self.assertEqual(EmployeeAvailability.objects.get().start_date, now)
        self.assertEqual(EmployeeAvailability.objects.get().end_date, future)


class TestCandidateViewSet(APITestCase):
    def setUp(self):
        self.candidate = mommy.make(Candidate)

    def test_retrieve_candidate(self):
        url = reverse('candidate-detail', kwargs={'pk': self.candidate.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Candidate.objects.count(), 1)
        self.assertEqual(Candidate.objects.get().name, self.candidate.name)

    def test_list_candidates(self):
        url = reverse('candidate-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Candidate.objects.count(), 1)
        self.assertEqual(Candidate.objects.get().name, self.candidate.name)

    def test_create_candidate_should_succeed(self):
        url = reverse('candidate-list')
        candidate_name = 'candidate 1'
        data = {'name': candidate_name}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        id = Candidate.objects.get(name=candidate_name).id
        self.assertEqual(response.data, {'id': id, 'name': candidate_name})
        self.assertEqual(Candidate.objects.count(), 2)
        self.assertEqual(Candidate.objects.get(name=candidate_name).name, candidate_name)

    def test_create_candidate_with_long_name_should_fail(self):
        url = reverse('candidate-list')
        candidate_name = 'this is a very long string that will not fit in the field inside db' * 10
        data = {'name': candidate_name}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Candidate.objects.count(), 1)

    def test_delete_on_the_list_is_405(self):
        url = reverse('candidate-list')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestCandidateAvailabilityViewSetAPI(APITestCase):
    def setUp(self):
        self.model = mommy.make(Candidate)

    def test_create_employee(self):
        now = datetime.now(pytz.utc)
        future = now + timedelta(days=1)
        url = reverse('candidate-timeslots-list', kwargs={'candidate_pk': self.model.id})
        data = {'start_date': now, 'end_date': future}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CandidateAvailability.objects.count(), 1)
        self.assertEqual(CandidateAvailability.objects.get().start_date, now)
        self.assertEqual(CandidateAvailability.objects.get().end_date, future)


class TestTimeSlots(APITestCase):
    def setUp(self):
        self.model = mommy.make(Candidate)

    def test_create_employee(self):
        now = datetime.now(pytz.utc)
        future = now + timedelta(days=1)
        url = reverse('candidate-timeslots-list', kwargs={'candidate_pk': self.model.id})
        data = {'start_date': now, 'end_date': future}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CandidateAvailability.objects.count(), 1)
        self.assertEqual(CandidateAvailability.objects.get().start_date, now)
        self.assertEqual(CandidateAvailability.objects.get().end_date, future)
