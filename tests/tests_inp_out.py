import os
import json
import inspect
import unittest
from executor import MarketRunner

from conf import settings
from utils import Utilities

PROJECT_ROOT = settings.PROJECT_ROOT


class StockMarketExecutionTest(unittest.TestCase):

    """
    Test cases being run:
    1. Input -> Output Validation
    2. Input length Validation
    """

    @classmethod
    def setUpClass(cls):
        # Extract expected input/output details from the following fixture
        fixtures_loc = os.path.join(PROJECT_ROOT, 'tests', 'fixtures', 'inp_out.json')
        cls.testing_data = json.load(open(fixtures_loc))

    def test_sample_input_output(self):
        # Fetch test configuration from fixtures
        function_name = inspect.stack()[0][3]
        test_conf = self.testing_data[function_name]

        runner_obj = MarketRunner()

        for i in test_conf['input']:
            runner_obj.execute(i)

        expected_transactions = Utilities.transform_transactions_for_comparison(test_conf['output'])
        received_transactions = Utilities.transform_transactions_for_comparison(runner_obj.transactions)

        if expected_transactions:
            intersection = set(expected_transactions).intersection(set(received_transactions))
            self.assertEqual(len(intersection), len(received_transactions))

    def test_wrong_length_input_error(self):
        # Fetch test configuration from fixtures
        function_name = inspect.stack()[0][3]
        test_conf = self.testing_data[function_name]

        for inp in test_conf['input']:
            try:
                Utilities.transform_input(inp)
            except Exception as ex:
                self.assertEqual(type(ex), AssertionError)

