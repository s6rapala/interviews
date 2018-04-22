from rest_framework import serializers

from interviews.models import EmployeeAvailability, Employee


class EmployeeAvailabilitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EmployeeAvailability
        fields = [
            'id',
            'start_date',
            'end_date',
            'employee_id',
        ]


class EmployeeSerializerDetail(serializers.HyperlinkedModelSerializer):
    timeslots = EmployeeAvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
            'timeslots',
        ]


class EmployeeSerializerList(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
        ]
