import unittest2

from torneira.testing.client import TestingClient

class TestingClientTestCase(unittest2.TestCase):
    def test_can_convert_dict_with_list_to_post_data(self):
        data = {
            'name': 'should be name',
            'status': 1,
            'itens': [1, 4, 3]
        }

        parsed_data = TestingClient.parse_post_data(data)
        self.assertTrue('status=1' in parsed_data)
        self.assertTrue('itens=1' in parsed_data)
        self.assertTrue('itens=4' in parsed_data)
        self.assertTrue('itens=3' in parsed_data)
        self.assertTrue('name=should+be+name' in parsed_data)
