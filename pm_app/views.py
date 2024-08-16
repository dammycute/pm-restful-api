from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['project_type', 'created_by']
    ordering_fields = ['start_date', 'end_date', 'created_at']

    @action(detail=True, methods=['post'])
    def add_team_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')
        if user_id:
            project.team_members.add(user_id)
            return Response({'status': 'team member added'})
        return Response({'status': 'error', 'message': 'user_id is required'}, status=400)

    @action(detail=True, methods=['delete'])
    def remove_team_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')
        if user_id:
            project.team_members.remove(user_id)
            return Response({'status': 'team member removed'})
        return Response({'status': 'error', 'message': 'user_id is required'}, status=400)