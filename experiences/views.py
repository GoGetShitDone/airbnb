from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Experience
from .serializers import ExperienceSerializer

class ExperienceViewSet(ModelViewSet):
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)