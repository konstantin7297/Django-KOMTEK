from sqlite3 import Date

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import RequestsClient

from .models import Directory, VersionDirectory, DirectoryElement


class DirectoryViewsCase(TestCase):
    """ Testing REST API endpoints """

    @classmethod
    def setUpClass(cls):
        cls.url = 'http://testserver'
        cls.factory = RequestsClient()
        cls.date = Date(year=1000, month=10, day=10)
        cls.directory, _ = Directory.objects.get_or_create(
            code="test_code",
            name="test_name",
            description="test_description",
        )
        cls.version_directory, _ = VersionDirectory.objects.get_or_create(
            directory=cls.directory,
            version="test_version",
            created_date=cls.date,
        )
        cls.directory_element, _ = DirectoryElement.objects.get_or_create(
            version_directory=cls.version_directory,
            code="test_code",
            value="test_value",
        )

    @classmethod
    def tearDownClass(cls):
        cls.directory_element.delete()
        cls.version_directory.delete()
        cls.directory.delete()

    def test_directory_view(self):
        url = self.url + reverse('service_api:directory-list')
        data = {"date": f"{self.date.year}-{self.date.month}-{self.date.day}"}
        response = self.factory.get(url, data=data)

        self.assertIn('refbooks', response.json())

        rows = response.json().get("refbooks")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].get("id"), self.directory.id)
        self.assertEqual(rows[0].get("code"), self.directory.code)
        self.assertEqual(rows[0].get("name"), self.directory.name)

    def test_directory_element_view(self):
        url = self.url + reverse(
            'service_api:element', kwargs={"id": self.directory.id}
        )
        data = {"version": self.version_directory.version}
        response = self.factory.get(url, data=data)

        self.assertIn('elements', response.json())

        rows = response.json().get("elements")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].get("code"), self.directory_element.code)
        self.assertEqual(rows[0].get("value"), self.directory_element.value)

    def test_directory_check_view(self):
        url = self.url + reverse('service_api:check', kwargs={"id": self.directory.id})
        params = {
            "code": self.directory_element.code,
            "value": self.directory_element.value,
            "version": self.version_directory.version,
        }
        response = self.factory.get(url, params=params)

        self.assertIn('exists', response.json())
        self.assertEqual(response.json().get("exists"), True)
