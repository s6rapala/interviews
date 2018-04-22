import collections
from collections import namedtuple

PossibleDates = collections.namedtuple('PossibleDates', 'employee_id start_date end_date')


def _calculate_intersection(interval1, interval2):
    """find intersection between two intervals"""
    employee_id, first_start, first_end = interval1
    employee_id, second_start, second_end = interval2

    if _has_intersection(first_start, first_end, second_start, second_end):
        start = first_start if first_start > second_start else second_start
        end = second_end if first_end > second_end else first_end
        return PossibleDates(employee_id, start, end)
    return None


def _has_intersection(first_start, first_end, seconds_start, second_end):
    return (seconds_start <= first_start <= second_end) \
           or (seconds_start <= first_end <= second_end) \
           or (first_start <= seconds_start <= first_end) \
           or (first_start <= second_end <= first_end)


def intersection(candidate_intervals, employee_intervals) -> list:
    """find intersections between two sets of intervals"""
    candidate_intervals = convert_to_named_tuple(candidate_intervals)
    employee_intervals = convert_to_named_tuple(employee_intervals)

    possible_dates = list()
    for c in candidate_intervals:
        for e in employee_intervals:
            result = _calculate_intersection(c, e)
            if result:
                assert isinstance(result, PossibleDates)
                # unlike standard python convention for _asdict() method underscore
                # does not discourage it's usage (see official documentation)
                possible_dates.append(dict(result._asdict()))
    return possible_dates


def convert_to_named_tuple(dicts: list) -> list:
    """converts list of dictionaries to list of named tuples"""
    return [namedtuple('Candidate', d.keys())(**d) for d in dicts]
