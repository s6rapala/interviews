from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from interviews.serializers import *


class CandidateAvailabilityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Candidate availability to be viewed or edited
    """
    serializer_class = CandidateAvailabilityListSerializer

    def get_queryset(self):
        return CandidateAvailability.objects.filter(candidate=self.kwargs['candidate_pk'])

    def perform_create(self, serializer):
        serializer.save(candidate_id=self.kwargs['candidate_pk'])


class CandidateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Candidate to be viewed or edited
    """
    queryset = Candidate.objects.all()
    serializer_class = CandidateListSerializer

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Candidate.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CandidateSerializerDetail(user)
        return Response(serializer.data)

