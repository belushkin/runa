import itertools

from rest_framework import serializers
from .models import Category
from common.util import flatten


class ChildListingField(serializers.RelatedField):

    def to_representation(self, value):
        serializer = CategorySerializer(
            instance=value
        )
        return serializer.data

    def to_internal_value(self, data):
        try:
            return flatten(data)
        except ValueError:
            raise serializers.ValidationError({
                'name': 'This field is required.'
            })


class CategorySerializer(serializers.ModelSerializer):
    children = ChildListingField(many=True, queryset=Category.objects.all())

    class Meta:
        model = Category
        fields = ['name', 'children']

    def to_representation(self, instance):

        if isinstance(instance, Category):
            ret = super().to_representation(instance)
            if not len(ret['children']):
                del ret['children']
            return ret

        return instance

    def create(self, validated_data):
        validated_data['children'] = list(itertools.chain.from_iterable(validated_data['children']))

        category = Category(name=validated_data.get('name'))
        category.save()
        categories = {category.name: category}

        for child in validated_data.get('children'):
            child_category = Category(name=child.get('name'), parent=categories.get(child.get('parent'))) \
                if child.get('parent') else Category(name=child.get('name'), parent=category)

            child_category.save()
            categories[child_category.name] = child_category

        return category

# class CategoriesSerializer(serializers.ListSerializer):
#
#     parents = CategorySerializer(many=True)
#     children = CategorySerializer(many=True)
#     siblings = CategorySerializer(many=True)
#
#     # def create(self, validated_data):
#     #     return Category.objects.create(**validated_data)
#     #
#     # def update(self, instance, validated_data):
#     #     instance.name = validated_data.get('name', instance.name)
#     #     # instance.parent = validated_data.get('parent', instance.code)
#     #     instance.save()
#     #
#     #     return instance
