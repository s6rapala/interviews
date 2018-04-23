from django.db import models
from django.utils.translation import gettext_lazy as _
# not sure why django docs insist on overwriting _, it's a useful python operator

# Create your models here.
from rest_framework.exceptions import ValidationError


class Employee(models.Model):
    # don't want to put employees and candidates in 1 one table
    # because later this will result in all kinds of different problems
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

    def save(self, *args, **kwargs):
        if self._state.adding and (self.start_date > self.end_date):
            raise ValidationError({'detail': _('Start date must be before end date')})
        super().save(*args, **kwargs)
