from django.db import models


# Create your models here.
class EmployeeAvailability(models.Model):
    id = models.AutoField(primary_key=True, )
    employee_name = models.CharField(max_length=20)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        pass  # TODO ID, date, time start, time end



