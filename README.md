[![stablebuild](https://travis-ci.org/stashkov/interviews.svg?branch=master)](https://travis-ci.org/stashkov/interviews)
[![codeclimate](https://codeclimate.com/github/stashkov/interviews/badges/gpa.svg)](https://codeclimate.com/github/stashkov/interviews/issues)
[![codecov](https://codecov.io/gh/stashkov/interviews/branch/master/graph/badge.svg)](https://codecov.io/gh/stashkov/interviews)

# Description
This application helps HR personnel to find
an appropriate time slot for candidates.
In other words, given a candidate and their time availability,
list all possible HR people who can interview this candidate.


# Installation
```shell
git clone this repo
cd interviews
virtualenv .
source bin/activate
pip install -r requiremenets.txt
```


# List of REST endpoints
#### Manage list of employees who make interviews
/employees
- GET - list all employees
- POST - create new employee


/employees/?name={employeeName}
- GET - search for employee with a specified name

/employees/?ordering=name
- GET - we don't really need this, but hey, it's a feature!

/employees/{employeeKey}
- GET - list available time slots for a specific employee
- DELETE - delete a specific employee
- PUT - update a specific employee

/employees/{employeeKey}/timeslots/
- GET - list available time slots for a specific employee
- POST - create a new time slot for a specific employee

/employees/{employeeKey}/timeslots/{timeslotKey}
- GET - show a specific timeslot for a specific employee
- PUT - update a new time slot for a specific employee


#### Manage list of candidates who take interviews
/candidates
- GET - list all candidates
- POST - create a new candidate


/candidates/{candidateKey}
- GET - list available time slots for a specific candidate
- DELETE - delete a specific candidate
- PUT - update a specific candidate

/candidates/{candidateKey}/timeslots/
- GET - list available time slots for a specific candidate
- POST - create a new time slot for a specific candidate

/candidates/{candidateKey}/timeslots/{timeslotKey}
- GET - show a specific timeslot for a specific candidate
- PUT - update a new time slot for a specific candidate



#### Receive a list of time slots to make an interview

Note: Providing a candidate and list of interviewers required.

/timeslots/?candidate_id={candidateKey}?employee_id={employeeKeys}
- GET - get available time slots for a specific candidate and a list of employees for next week


/timeslots/?candidate_id={candidateKey}?employee_id={employeeKeys}&start_date={start_date}&end_date={end_date}/
- GET - get available time slots for a specific candidate and a list of emplyees for specific dates
