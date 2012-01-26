import unittest2

from torneira.testing.client import TestingClient

class TestingClientTestCase(unittest2.TestCase):
    def test_can_convert_dict_wtih_list_to_post_data(self):
        data = {
            'name': 'should be name',
            'status': 1,
            'itens': [1, 4, 3]
        }

        parsed_data = TestingClient.parse_post_data(data)
        expected_data = 'status=1&itens=1&itens=4&itens=3&name=should+be+name'
        self.assertEquals(parsed_data, expected_data)
