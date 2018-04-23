from django.db import models


# Create your models here.


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'id:{self.id} name:{self.name}'


class EmployeeAvailability(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, related_name='timeslots', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        unique_together = [
            ('employee', 'start_date', 'end_date'),
        ]

    def __str__(self):
        return f'{self.employee.name} is available from {self.start_date:%b-%d %H:%M} to {self.end_date:%b-%d %H:%M}'
