from django.db import models


# Create your models here.


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)


class EmployeeAvailability(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, related_name='timeslots', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    # TODO primary key should be a composite key of employee_id, start_date, end_date

    def __str__(self):
        return f"{self.employee.name} is available on {self.start_date}"
