import itertools

from rest_framework import serializers
from django.db import transaction
from .models import Category
from common.util import flatten


class ChildListingField(serializers.RelatedField):
    """
    Children field serializer is used for flattening incoming nested tree to flat list with previous parent
    """

    def to_internal_value(self, data):
        """
        Hook for transforming representation to internal values, used also for validation
        :arg
            data (:obj:`dict`): children categories
        :raises:
            serializers.ValidationError: if name is empty or missed
        """
        try:
            return flatten(data)
        except ValueError:
            raise serializers.ValidationError({
                'name': 'This field is required.'
            })


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer is used when new json with categories is submitted to the API
    Used for POST request
    """

    children = ChildListingField(many=True, queryset=Category.objects.all(), required=False)

    class Meta:
        model = Category
        fields = ['name', 'children']

    @transaction.atomic()
    def create(self, validated_data):
        """
        After validation phase, this method operates on valid data and store categories to the storage
        This method is transactional
        :arg
            validated_data (:obj:`dict`): dict with flatten and prepared data for storing
        :returns:
            Category model object
        """
        validated_data['children'] = list(itertools.chain.from_iterable(validated_data.get('children', [])))
        category = Category(name=validated_data.get('name'))
        category.save()
        categories = {category.name: category}

        for child in validated_data.get('children'):
            child_category = Category(name=child.get('name'), parent=categories.get(child.get('parent'))) \
                if child.get('parent') else Category(name=child.get('name'), parent=category)

            child_category.save()
            categories[child_category.name] = child_category

        return category


class CategoryShortSerializer(serializers.ModelSerializer):
    """
    Short serializer is used for representation of the each category
    """

    class Meta:
        model = Category
        fields = ['id', 'name']


class CategoriesSerializer(serializers.ModelSerializer):
    """
    Short serializer is used for representation of the each category
    Used for GET request
    """

    parents = serializers.SerializerMethodField(method_name="get_parents")
    children = serializers.SerializerMethodField(method_name="get_children")
    siblings = serializers.SerializerMethodField(method_name="get_siblings")

    class Meta:
        model = Category
        fields = ['id', 'name', 'parents', 'children', 'siblings']

    def get_parents(self, obj):
        serializer = CategoryShortSerializer(
            instance=self._get_parents_tree(obj),
            many=True
        )
        return serializer.data

    def get_children(self, obj):
        serializer = CategoryShortSerializer(
            instance=obj.children.all(),
            many=True
        )
        return serializer.data

    def get_siblings(self, obj):
        serializer = CategoryShortSerializer(
            instance=Category.objects.filter(parent=obj.parent).exclude(pk=obj.pk),
            many=True
        )
        return serializer.data

    def _get_parents_tree(self, obj):
        categories = []
        category = obj.parent
        while category is not None:
            categories.append(category)
            category = category.parent

        return categories
