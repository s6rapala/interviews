from django.db import models


# Create your models here.
class EmployeeAvailability(models.Model):
    id = models.IntegerField(primary_key=True)
    employee_id = models.IntegerField()  # foreign key to employee table
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class CandidateAvailability(models.Model):
    id = models.IntegerField(primary_key=True)
    candidate_id = models.IntegerField()  # foreign key to candidate table
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()



