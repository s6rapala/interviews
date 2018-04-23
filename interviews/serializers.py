from rest_framework import serializers

from interviews.models import EmployeeAvailability, Employee, Candidate, CandidateAvailability


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


class CandidateListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            'id',
            'name',
        ]


class CandidateAvailabilityListSerializer(serializers.HyperlinkedModelSerializer):
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
