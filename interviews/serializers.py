import copy

from rest_framework import serializers

from interviews.models import EmployeeAvailability, Employee, Candidate, CandidateAvailability
from interviews.utils import start_date_of_next_week, end_date_of_next_week


class StartDateEndDateOrderChecker:
    def validate(self, data):
        if ('start_date' in data and 'end_date' in data) and data['start_date'] > data['end_date']:
            raise serializers.ValidationError("start_date must occur after end_date")
        return data


class EmployeeAvailabilityListSerializer(StartDateEndDateOrderChecker, serializers.HyperlinkedModelSerializer):
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


class CandidateListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            'id',
            'name',
        ]


class CandidateAvailabilityListSerializer(StartDateEndDateOrderChecker, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CandidateAvailability
        fields = [
            'id',
            'start_date',
            'end_date',
            'candidate_id',
        ]


class CandidateSerializerDetail(serializers.HyperlinkedModelSerializer):
    timeslots = CandidateAvailabilityListSerializer(many=True, read_only=True)

    def update(self, **kwargs):
        pass

    class Meta:
        model = Candidate
        fields = [
            'id',
            'name',
            'timeslots',
        ]


class AvailableTimeSlotsListSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class TimeSlotsSerializerInput(serializers.Serializer):
    candidate_id = serializers.IntegerField()
    employee_id = serializers.ListField(child=serializers.IntegerField())
    start_date = serializers.DateTimeField(required=False, default=start_date_of_next_week())
    end_date = serializers.DateTimeField(required=False, default=end_date_of_next_week())

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def to_internal_value(self, data):
        data = copy.copy(dict(data))  # shallow copy is sufficient (no need for deepcopy)
        # TODO query_param always come as a list from URL; better way for this [0] nonsense
        data = {k: v[0] for k, v in data.items()}
        try:
            data['employee_id'] = [int(i) for i in data['employee_id'].split(',')]
        except (ValueError, KeyError):
            pass  # validator throw the error if it find it
        return super().to_internal_value(data)
