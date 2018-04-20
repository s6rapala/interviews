# Synopsis
This application helps HR personnel to find
an appropriate time slot for candidates.
In other words, given a candidate and their time availability,
list all possible HR people who can interview this candidate.


# List of REST endpoints
#### Manage list of employees who make interviews
/employees
- GET - get list of all employees
- POST - create new employee
- DELETE - delete employee
- PUT - update employee

/candidates/{employeeKey}
- GET - get available time slots for a specific employee
- POST - create new time slot for a specific employee
- DELETE - delete time slot for a specific employee
- PUT - update time slot for a specific employee


#### Manage list of candidates who take interviews
/candidates
- GET - get list of all candidates
- POST - create new candidate
- DELETE - delete candidate
- PUT - update candidate


/candidates/{candidateKey}
- GET - get available time slots for a specific candidate
- POST - create new time slot for a specific candidate
- DELETE - delete time slot for a specific candidate
- PUT - update time slot for a specific candidate


#### Receive a list of time slots to make an interview
/timesheet?candidateKey={candidateKey}?employeeKeys={employeeKeys}
- GET
(providing a candidate and list of interviewers required).