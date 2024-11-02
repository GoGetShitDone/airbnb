from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Category
from .serializers import CategorySerializer

class Categories(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # 읽기는 모두 가능, 쓰기는 인증된 사용자만

    def get(self, request):
        # rooms 카테고리만 필터링
        categories = Category.objects.filter(
            kind=Category.CategoryKindChoices.ROOMS
        )
        serializer = CategorySerializer(
            categories,
            many=True,
        )
        return Response(serializer.data)
    
    def post(self, request):
        # POST는 관리자만 가능하도록
        if not request.user.is_staff:
            raise PermissionDenied
        
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return Response(CategorySerializer(category).data)
        else:
            return Response(serializer.errors)

class CategoryDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound
            
    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
        
    def put(self, request, pk):
        # PUT은 관리자만 가능하도록
        if not request.user.is_staff:
            raise PermissionDenied
            
        category = self.get_object(pk)
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)
            
    def delete(self, request, pk):
        # DELETE는 관리자만 가능하도록
        if not request.user.is_staff:
            raise PermissionDenied
            
        category = self.get_object(pk)
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)