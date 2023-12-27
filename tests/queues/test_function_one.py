from unittest import TestCase
from queues import function_one


class TestFunctionOne(TestCase):
    def test_main(self):
        self.assertEqual(
            function_one.main(
                query_params={'query_param_one': 'query_param_one_value'},
                body={'body_one': 'body_one_value'}
            ),
            {
                'statusCode': 200,
                'body': '{"message": "function_one", "query_params": {"query_param_one": "query_param_one_value"}, '
                        '"body": {"body_one": "body_one_value"}}'
            }
        )
