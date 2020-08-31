from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CategoriesSerializer
from .models import Category


class Categories(APIView):
    def post(self, request):
        queryset = Category.objects.all()
        serializer_class = CategoriesSerializer

