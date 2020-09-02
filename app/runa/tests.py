import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from runa.models import Category


class CategoryTests(APITestCase):
    def test_create_list_of_catefories_when_db_is_empty(self):
        """
        Ensure we can create a new categories objects.
        """
        # given
        data = {'name': 'c1', 'children': [{'name': 'c2'}, {'name': 'c3'}]}

        # when
        response = self.client.post(reverse('add_categories'), data, format='json')

        # then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Category.objects.filter(parent=None).count(), 1)

    def test_create_category_with_the_same_name_gives_an_error(self):
        """
        Ensure we can't create a new category object with the same name.
        """
        # given
        data = {'name': 'c1'}

        # when
        self.client.post(reverse('add_categories'), data, format='json')
        response = self.client.post(reverse('add_categories'), data, format='json')

        # then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_category_without_children(self):
        """
        Ensure we can create category without children
        """
        # given
        data = {"name": "c1"}

        # when
        response = self.client.post(reverse('add_categories'), data, format='json')

        # then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)

    def test_create_category_with_wrong_data_does_not_create_anything(self):
        """
        Ensure we would not create anything if data is wrong
        """
        # given
        data = {"title": "c1", "siblings": []}

        # when
        response = self.client.post(reverse('add_categories'), data, format='json')

        # then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_categories_and_check_structure_of_categories(self):
        """
        Ensure the returned structure
        """
        # given
        with open('runa/fixtures/fixture.json') as json_file:
            data = json.load(json_file)
        with open('runa/fixtures/2.json') as json_file:
            second_category = json.load(json_file)
        with open('runa/fixtures/8.json') as json_file:
            eight_category = json.load(json_file)

        # when
        self.client.post(reverse('add_categories'), data, format='json')
        second_response = self.client.get(reverse('list_category', args=[2]))
        eight_response = self.client.get(reverse('list_category', args=[8]))

        # then
        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(second_response.content, second_category)
        self.assertJSONEqual(eight_response.content, eight_category)
