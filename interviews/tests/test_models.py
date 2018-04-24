from django.test import TestCase
from model_mommy import mommy

from interviews.models import Employee, EmployeeAvailability, CandidateAvailability, Candidate


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


class TestCandidate(TestCase):
    def setUp(self):
        self.models = mommy.make(Candidate)

    def test_str(self):
        self.assertEquals(str(self.models), f'id:{self.models.id} name:{self.models.name}')


class TestCandidateAvailability(TestCase):
    def setUp(self):
        self.models = mommy.make(CandidateAvailability)

    def test_str(self):
        self.assertEquals(str(self.models),
                          f'{self.models.candidate.name} is available from '
                          f'{self.models.start_date:%b-%d %H:%M} '
                          f'to {self.models.end_date:%b-%d %H:%M}')
