# coding: utf-8
from torneira.cache.util import cache_key, cached

from tests.util import unittest


class MySimpleObject(object):
    @cached
    def do_something(self, a, b):
        return a + b


class MyModel(object):
    id = None

    def __init__(self, id_):
        self.id = id_

    @cached
    def do_something(self, a, b):
        return a + b


class ObjectWithSpecialMethod(object):
    # just to ensure that cache_key will not use this value
    id = 'should-not-be-used'
    _my_value = None

    def __init__(self, value):
        self._my_value = value

    def get_cache_key(self):
        return self._my_value

    @cached
    def do_something(a, b):
        return a + b


class GenerateCacheKeyTestCase(unittest.TestCase):
    def test_generate_cache_key_for_simple_object(self):
        my_instance = MySimpleObject()

        fn_kwargs = {'a': 1, 'b': 2}
        _, generated_key = cache_key(my_instance, 'do_something', **fn_kwargs)
        expected_key = 'tests.cache.test_extension.MySimpleObject().do_something(a=1,b=2)'

        self.assertEqual(generated_key, expected_key)

    def test_generate_cache_key_for_model_object(self):
        my_instance = MyModel("unique-id-1")

        fn_kwargs = {'a': 1, 'b': 2}
        _, generated_key = cache_key(my_instance, 'do_something', **fn_kwargs)
        expected_key = 'tests.cache.test_extension.MyModel(unique-id-1).do_something(a=1,b=2)'

        self.assertEqual(generated_key, expected_key)

    def test_generate_cache_key_for_object_with_special_method(self):
        my_instance = ObjectWithSpecialMethod('unique-value')

        fn_kwargs = {'a': 1, 'b': 2}
        _, generated_key = cache_key(my_instance, 'do_something', **fn_kwargs)
        expected_key = 'tests.cache.test_extension.ObjectWithSpecialMethod(unique-value).do_something(a=1,b=2)'

        self.assertEqual(generated_key, expected_key)
