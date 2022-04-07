import json
from unittest import TestCase

from django.test import Client


class APITests(TestCase):

    def setUp(self):
        self.client = Client()
        super(APITests, self).setUp()

    def test_get_limits_successful(self):
        """Test successful get limits."""
        self.client.login(username='user_120', password='password')
        response = self.client.get('/limits/')
        result_fixture = {
            'months': {
                'timestamp': {'minimum': '2014-06-01', 'maximum': '2015-12-01'},
                'consumption': {'minimum': 854, 'maximum': 1108},
                'temperature': {'minimum': 3, 'maximum': 14}},
            'days': {
                'timestamp': {'minimum': '2014-11-01', 'maximum': '2015-12-30'},
                'consumption': {'minimum': 5, 'maximum': 59},
                'temperature': {'minimum': -12, 'maximum': 31}
            }
        }
        self.assertEqual(json.loads(response.content.decode()), result_fixture)

    def test_get_limits_not_logged_in(self):
        """"Test get limits of not logged in user."""
        response = self.client.get('/limits/')
        self.assertEqual(response.status_code,  302)

    def test_get_data_months_successful(self):
        """Test data by months successful."""
        client = Client()
        client.login(username='user_120', password='password')
        response = client.get('/data/', {'start': '2014-07-01', 'count': '4', 'resolution': 'M'})
        result_fixture = {
            'data': [
                ['2014-07-01', 901, 11],
                ['2014-08-01', 875, 10],
                ['2014-09-01', 901, 11],
                ['2014-10-01', 854, 8],
            ]
        }

        self.assertEqual(json.loads(response.content.decode()), result_fixture)

    def test_get_data_days_successful(self):
        """Test data by days successful."""
        self.client.login(username='user_120', password='password')
        response = self.client.get('/data/', {'start': '2014-11-02', 'count': '4', 'resolution': 'D'})
        result_fixture = {
            'data': [
                ['2014-11-02', 18, 20],
                ['2014-11-03', 44, 13],
                ['2014-11-04', 31, -11],
                ['2014-11-05', 36, 2]
            ]
        }

        self.assertEqual(json.loads(response.content.decode()), result_fixture)

    def test_get_data_days_successful_part(self):
        """Test data by days successful with not days in range."""
        self.client.login(username='user_120', password='password')
        response = self.client.get('/data/', {'start': '2015-12-29', 'count': '4', 'resolution': 'D'})
        result_fixture = {
            'data': [
                ['2015-12-29', 19, -1],
                ['2015-12-30', 41, 25]
            ]
        }

        self.assertEqual(json.loads(response.content.decode()), result_fixture)

    def test_get_data_days_successful_no_data(self):
        """Test data by days successful with no data in range."""
        self.client.login(username='user_120', password='password')
        response = self.client.get('/data/', {'start': '2012-12-29', 'count': '4', 'resolution': 'D'})
        result_fixture = {
            'data': []
        }

        self.assertEqual(json.loads(response.content.decode()), result_fixture)

    def test_get_data_not_all_fields(self):
        """Test data by days validation error not all required fields."""
        self.client.login(username='user_120', password='password')
        response = self.client.get('/data/', {'start': '2014-11-02', 'resolution': 'D'})
        self.assertEqual(response.content.decode(), '"start_date", "count" and "resolution" are required.')

    def test_get_data_wrong_date_format(self):
        """Test data by days validation error date in wrong format."""
        self.client.login(username='user_120', password='password')
        response = self.client.get('/data/', {'start': '2014-20-02', 'count': '4', 'resolution': 'D'})
        self.assertEqual(response.content.decode(),
                         'Start date 2014-20-02 is not valid. Please provide it in format: %Y-%m-%d.')

    def test_get_data_wrong_count_format(self):
        """Test data by days validation error count in wrong format."""
        self.client.login(username='user_120', password='password')
        response = self.client.get('/data/', {'start': '2014-11-02', 'count': 'a', 'resolution': 'D'})
        self.assertEqual(response.content.decode(), 'Count a is not valid. Please provide it as positive integer.')

    def test_get_data_wrong_resolution_format(self):
        """Test data by days validation error resolution in wrong format."""
        self.client.login(username='user_120', password='password')
        response = self.client.get('/data/', {'start': '2014-11-02', 'count': '4', 'resolution': 'W'})
        self.assertEqual(response.content.decode(), 'Resolution should be "M" (month) or "D" (day).')
