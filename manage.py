import os
import sys
dirloc = os.path.abspath(os.path.dirname(__file__))
sys.path.append(dirloc)

from argparse import ArgumentParser

from executor import MarketRunner
from utils import Utilities

from tests.tests_field_validations import StockMarketFieldsTest
from tests.tests_inp_out import StockMarketExecutionTest


if __name__ == '__main__':
    parser = ArgumentParser(description="Stock Exchange.")
    parser.add_argument('run_as', choices=['test', 'production'], default='production', help='Run as')
    args = parser.parse_args()

    if args.run_as == 'test':
        test_classes = [StockMarketFieldsTest, StockMarketExecutionTest]
        Utilities.run_multiple_test_cases(test_classes)
    elif args.run_as == 'production':
        runner = MarketRunner()
        
        while True:
            line = raw_input()
            if line:
                transformed = Utilities.transform_input(line)
                runner.execute(transformed)
            else:
                break
        
        print "Transactions:"
        Utilities.print_transactions(runner.transactions)
        print "Pending:"
        Utilities.print_pending(runner.pending)