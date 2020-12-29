#!/usr/bin/env python
"""Unit test for api module GraphQL queries."""
import requests
import unittest

class TestApi(unittest.TestCase):
    """Class to execute unit tests for Entity_api.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.base_url = 'http://127.0.0.1:5000/graphql'
        self.headers = {'content-type': 'application/json'}

    def test_query_accound_id(self):
        # Get batch list
        payload = '{"query": "{account(id:\\"QWNjb3VudE5vZGU6MQ==\\"){id_name}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        print(json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['data']['account']['id_name'], 'denis')

    def test_query_find_name_passord(self):
        # Get batch list
        payload = '{"query": "{findAccount  (id_name:\\"denis\\", password:\\"1234\\"){id}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        print(json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['data']['findAccount']['id'], 'QWNjb3VudE5vZGU6MQ==')
    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        pass


if __name__ == '__main__':
    # Test api endpoints
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApi)
    unittest.TextTestRunner(verbosity=2).run(suite)