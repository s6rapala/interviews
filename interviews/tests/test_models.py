from datetime import datetime, timedelta

from django.test import TestCase
from model_mommy import mommy
from rest_framework.exceptions import ValidationError

from interviews.models import Employee, EmployeeAvailability


class TestEmployee(TestCase):
    def setUp(self):
        self.models = mommy.make(Employee)

    def test_str(self):
        self.assertEquals(str(self.models), f'id:{self.models.id} name:{self.models.name}')


class TestEmployeeAvailability(TestCase):
    def setUp(self):
        self.models = mommy.make(EmployeeAvailability)

    def test_str(self):
        self.assertEquals(str(self.models),
                          f'{self.models.employee.name} is available from '
                          f'{self.models.start_date:%b-%d %H:%M} '
                          f'to {self.models.end_date:%b-%d %H:%M}')

    def test_end_date_in_the_past_raises_value_error(self):
        model = EmployeeAvailability(employee_id=self.models.employee.id,
                                     start_date=datetime.now(),
                                     end_date=datetime.now() + timedelta(days=-1))
        with self.assertRaises(ValidationError):
            model.save()
