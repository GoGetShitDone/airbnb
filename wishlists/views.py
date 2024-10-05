from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Wishlist
from .serializers import WishlistSerializer

class WishlistViewSet(ModelViewSet):
    serializer_class = WishlistSerializer
    queryset = Wishlist.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)