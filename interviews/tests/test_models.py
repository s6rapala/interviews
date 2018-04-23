from django.test import TestCase
from model_mommy import mommy

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
        print(str(self.models))
        self.assertEquals(str(self.models),
                          f'{self.models.employee.name} is available from '
                          f'{self.models.start_date:%b-%d %H:%M} '
                          f'to {self.models.end_date:%b-%d %H:%M}')
