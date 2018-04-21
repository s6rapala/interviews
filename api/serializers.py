from rest_framework import serializers

from interviews.models import EmployeeAvailability


class EmployeeAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAvailability
        fields = [
            'employee_name',
            'start_date',
            'end_date',
            'id',
        ]
