from django.http import Http404
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
        # TODO this validator breaks other behaviour of this Serializer. Very strange.
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=model.objects.all(),
        #         fields=('employee_id', 'start_date', 'end_date'),
        #         message=("Some custom message.")
        #     )
        # ]


class EmployeeSerializerDetail(serializers.HyperlinkedModelSerializer):
    timeslots = EmployeeAvailabilityListSerializer(many=True, read_only=True)

    def update(self, **kwargs):
        pass

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


class AvailableTimeSlotsListSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
