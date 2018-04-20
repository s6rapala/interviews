from django.db import models


# Create your models here.
class EmployeeAvailability(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        pass  # TODO ID, date, time start, time end


class CandidateAvailability(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()



