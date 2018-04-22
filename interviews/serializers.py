from rest_framework import serializers

from interviews.models import EmployeeAvailability, Employee


class EmployeeAvailabilityListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EmployeeAvailability
        fields = [
            'id',
            'start_date',
            'end_date',
            'employee_id',
        ]


class EmployeeSerializerDetail(serializers.HyperlinkedModelSerializer):
    timeslots = EmployeeAvailabilityListSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
            'timeslots',
        ]


class EmployeeListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
        ]
