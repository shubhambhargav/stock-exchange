import unittest
from datetime import time

from conf import settings

INPUT_FIELDS = settings.INPUT_FIELDS


class Utilities(object):

    @staticmethod
    def transform_input(line):
        vals = line.split(' ')
        assert len(vals) == 6, "Invalid input length: expected '6', found '%s'" % len(vals)

        return dict(zip(INPUT_FIELDS, vals))

    @staticmethod
    def print_transactions(l):
        for e in l:
            print "%(sell_order_id)s %(quantity)s %(sell_price)s %(buy_order_id)s" % e

    @staticmethod
    def print_pending(d):
        l = []
        
        for action, action_data in d.items():
            for stock_name, order_data in action_data.items():
                for order_id, data in order_data.items():
                    price, timeval, _, quantity = data
                    l.append({
                                'order_id': order_id,
                                'stock': stock_name,
                                'action': action,
                                'timeval': time.strftime(timeval, '%H:%M'),
                                'price': price,
                                'quantity': quantity
                            })

        for e in l:
            print "%(order_id)s %(timeval)s %(stock)s %(action)s %(quantity)s %(price)s" % e

    @staticmethod
    def transform_transactions_for_comparison(l):
        transformed = []
        for e in l:
            transformed.append("%(sell_order_id)s %(quantity)s %(sell_price)s %(buy_order_id)s" % e)

        return transformed

    @staticmethod
    def run_multiple_test_cases(test_class_list):
        loader = unittest.TestLoader()

        suites_list = []
        for t in test_class_list:
            small_suite = loader.loadTestsFromTestCase(t)
            suites_list.append(small_suite)

        big_suite = unittest.TestSuite(suites_list)
        runner = unittest.TextTestRunner()
        runner.run(big_suite)




