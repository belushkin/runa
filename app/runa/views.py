from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import CategorySerializer, CategoriesSerializer
from .models import Category


class CategoriesList(APIView):

    def get(self, request):
        categories = Category.objects.filter(parent=None)
        serializer = CategorySerializer(categories, many=True) \
            if len(categories) > 1 else \
            CategorySerializer(categories.first())

        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'ok': True}, status=201)

        return JsonResponse(serializer.errors, status=400)


class CategoryDetail(APIView):

    def get(self, request, pk, format=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return HttpResponse(status=404)

        serializer = CategoriesSerializer(category)
        return JsonResponse(serializer.data)
