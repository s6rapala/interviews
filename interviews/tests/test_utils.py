from datetime import datetime, timedelta
from unittest import TestCase

from interviews.utils import intersection, start_and_end_date_of_next_week


class TestIntersection(TestCase):
    """
    Essentially this class should covers all 13 relations between 2 intervals
    https://en.wikipedia.org/wiki/Allen%27s_interval_algebra
    and on top of that relations with > 2 intervals
    """
    CANDIDATE_ID = 1  # can only be exactly 1
    EMPLOYEE_ID = 2  #

    def test_intersection_equals(self):
        now = datetime.now()
        future = now + timedelta(days=1)

        interval1 = [{'employee_id': self.CANDIDATE_ID, 'start_date': now, 'end_date': future}]
        interval2 = [{'employee_id': self.EMPLOYEE_ID, 'start_date': now, 'end_date': future}]

        result = intersection(interval1, interval2)
        self.assertTrue(isinstance(result, list))
        self.assertTrue(isinstance(result[0], dict))

        self.assertEquals(result[0]['employee_id'], self.EMPLOYEE_ID)
        self.assertEquals(result[0]['start_date'], now)
        self.assertEquals(result[0]['end_date'], future)

    def test_intersection_employee_contains_candidate(self):
        now = datetime.now()
        future = now + timedelta(days=1)

        interval1 = [{'employee_id': self.CANDIDATE_ID,
                      'start_date': now + timedelta(days=-1),
                      'end_date': future + timedelta(days=1)}]
        interval2 = [{'employee_id': self.EMPLOYEE_ID,
                      'start_date': now,
                      'end_date': future}]

        result = intersection(interval1, interval2)
        self.assertTrue(isinstance(result, list))
        self.assertTrue(isinstance(result[0], dict))

        self.assertEquals(result[0]['employee_id'], self.EMPLOYEE_ID)
        self.assertEquals(result[0]['start_date'], now)
        self.assertEquals(result[0]['end_date'], future)

    def test_intersection_candidate_contains_employee(self):
        now = datetime.now()
        future = now + timedelta(days=1)

        interval1 = [{'employee_id': self.CANDIDATE_ID,
                      'start_date': now,
                      'end_date': future}]
        interval2 = [{'employee_id': self.EMPLOYEE_ID,
                      'start_date': now + timedelta(days=-1),
                      'end_date': future + timedelta(days=1)}]

        result = intersection(interval1, interval2)
        self.assertTrue(isinstance(result, list))
        self.assertTrue(isinstance(result[0], dict))

        self.assertEquals(result[0]['employee_id'], self.EMPLOYEE_ID)
        self.assertEquals(result[0]['start_date'], now)
        self.assertEquals(result[0]['end_date'], future)

    def test_intersection_no_common_time(self):
        now = datetime.now()
        future = now + timedelta(days=1)

        interval1 = [{'employee_id': self.CANDIDATE_ID,
                      'start_date': now,
                      'end_date': future}]
        interval2 = [{'employee_id': self.EMPLOYEE_ID,
                      'start_date': now + timedelta(days=100),
                      'end_date': future + timedelta(days=100)}]

        result = intersection(interval1, interval2)
        self.assertTrue(isinstance(result, list))
        self.assertFalse(bool(result))


class TestNextWeekDatesGenerator(TestCase):
    def test_start_and_end_date_of_next_week(self):
        tuesday = datetime(2018, 4, 24)
        next_monday = datetime(2018, 4, 30, 0, 0)
        next_saturday = datetime(2018, 5, 6, 23, 59)
        self.assertEquals(start_and_end_date_of_next_week(tuesday), (next_monday, next_saturday))
