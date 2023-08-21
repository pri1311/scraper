from django.test import TestCase
from django.urls import reverse
import json
import re


class Config:
    URL = "https://en.wikipedia.org/wiki/India_national_football_team"
    SPECIAL_CHAR_URL = "https://www.ibm.com/docs/en/zos/2.4.0?topic=commands-alphanumeric-national-special-characters"
    FILENAME = "football.txt"
    DEFAULT_FILENAME = "data.txt"


config = Config()


class ScraperTests(TestCase):
    def test_successful_extraction(self):
        response = self.client.post(reverse('extract'), {'url': config.URL})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                         "message": "Data stored in file data.txt"})

    def test_successful_extraction_with_filename(self):
        response = self.client.post(
            reverse('extract'), {'url': config.URL, 'fileName': config.FILENAME})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                         "message": "Data stored in file football.txt"})

    def test_missing_url(self):
        response = self.client.post(reverse('extract'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
                         'error': 'URL is required. Attach the URL with the body of the POST request under key `url`'})

    def test_remove_special_characters_true(self):
        response = self.client.post(
            reverse('extract'),
            {'url': config.SPECIAL_CHAR_URL, 'remove_special_characters': True},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        file = open(config.DEFAULT_FILENAME, "r")
        data = re.sub(r"[\n\t\s]*", "", file.read())
        self.assertEqual(all(i.strip("\n\t ").isalnum() for i in data), True)

    def test_remove_special_characters_false(self):
        response = self.client.post(
            reverse('extract'), {'url': config.SPECIAL_CHAR_URL})
        self.assertEqual(response.status_code, 200)
        file = open(config.DEFAULT_FILENAME, "r")
        data = file.read()
        self.assertEqual(any(not i.isalnum() for i in data), True)

    def test_to_lowercase_true(self):
        response = self.client.post(
            reverse('extract'),
            {'url': config.SPECIAL_CHAR_URL, 'to_lowercase': True},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        file = open(config.DEFAULT_FILENAME, "r")
        data = file.read()
        self.assertEqual(data.islower(), True)

    def test_to_lowercase_false(self):
        response = self.client.post(
            reverse('extract'), {'url': config.SPECIAL_CHAR_URL})
        self.assertEqual(response.status_code, 200)
        file = open(config.DEFAULT_FILENAME, "r")
        data = file.read()
        self.assertEqual(not data.islower(), True)
