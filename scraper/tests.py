from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse


class ScraperTests(TestCase):
    def test_successful_extraction(self):
        url = "https://en.wikipedia.org/wiki/India_national_football_team"
        response = self.client.post(reverse('extract'), {'url': url})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                         "message": "Data stored in file data.txt"})

    def test_successful_extraction_with_filename(self):
        url = "https://en.wikipedia.org/wiki/India_national_football_team"
        fileName = "football.txt"
        response = self.client.post(
            reverse('extract'), {'url': url, 'fileName': fileName})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                         "message": "Data stored in file football.txt"})

    def test_missing_url(self):
        response = self.client.post(reverse('extract'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
                         'error': 'URL is required. Attach the URL with the body of the POST request under key `url`'})
