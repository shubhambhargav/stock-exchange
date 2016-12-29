from db.models import StockMarket
from db.fields import IntField, TimeField, CharField, ChoiceField, FloatField
from utils import Utilities


class MarketRunner(StockMarket):

    order_id = IntField(inp='order_id')
    timeval = TimeField(inp='timeval', time_format='%H:%M')
    stock = CharField(inp='stock')
    action = ChoiceField(inp='action', choices=['buy', 'sell'])
    price = FloatField(inp='price')

    quantity = IntField(inp='quantity', out='quantity')

    sell_price = FloatField(out='sell_price')
    buy_order_id = IntField(out='buy_order_id')
    sell_order_id = IntField(out='sell_order_id')

    def __init__(self, *args, **kwargs):
        super(MarketRunner, self).__init__(*args, **kwargs)

        self.pending = {'buy': {}, 'sell': {}}

    def process_data(self, native_object):
        order_id = native_object['order_id']
        stock_name = native_object['stock']
        price = native_object['price']
        quantity = native_object['quantity']
        action = native_object['action']

        transactions = []

        if action == 'sell':
            # Filter the corresponding buy options which have higher price than currrent sell
            filtered_sells = [v for v in self.pending['buy'].get(stock_name, {}).values() if v[0] > price]
            # Sort extracted data by price, time, order_id in the order
            sorted_sells = sorted(filtered_sells, key=lambda x: [x[0], x[1], x[2]])

            """
            Following code takes care of 3 possible scenarios for each available option of buy:
            1. If quantity_sell < quantity_buy
                then 
                    1.. decrement the quantity of buy by quantity sell
                    2.. append a completed transaction
                    3.. break
            2. If quantity_sell = quantity_buy
                then 
                    1.. delete the standing option of buy from pending list
                    2.. append a completed transaction
                    3.. break
            3. If quantity_sell > quantity_buy
                then
                    1.. decrement the quantity of sell by quantity
                    2.. delete the standing option of buy from pending list
                    3.. continue the process
            """

            for elem in sorted_sells:
                quantity_buy = elem[3]

                if quantity < quantity_buy:
                    transactions.append({
                                        'sell_order_id': order_id,
                                        'buy_order_id': elem[2],
                                        'quantity': quantity,
                                        'sell_price': price
                                        })
                    self.pending['buy'][stock_name][elem[2]][3] -= quantity
                    quantity = 0
                    break
                elif quantity == quantity_buy:
                    transactions.append({
                                        'sell_order_id': order_id,
                                        'buy_order_id': elem[2],
                                        'quantity': quantity,
                                        'sell_price': price
                                        })
                    del self.pending['buy'][stock_name][elem[2]]
                    quantity = 0
                    break
                elif quantity > quantity_buy:
                    transactions.append({
                                        'sell_order_id': order_id,
                                        'buy_order_id': elem[2],
                                        'quantity': quantity_buy,
                                        'sell_price': price
                                        })
                    quantity -= quantity_buy
                    del self.pending['buy'][stock_name][elem[2]]

        elif action == 'buy':
            # Filter the corresponding sell options which have lower price than currrent buy
            filtered_sells = [v for v in self.pending['sell'].get(stock_name, {}).values() if v[0] < price]
            # Sort extracted data by price, time, order_id in the order
            sorted_sells = sorted(filtered_sells, key=lambda x: [x[0], x[1], x[2]])

            """
            Following code follows the same logic as followed by sell option.
            Please refer to lines 40-57
            """

            for elem in sorted_sells:
                quantity_sell = elem[3]

                if quantity < quantity_sell:
                    transactions.append({
                                        'sell_order_id': elem[2],
                                        'buy_order_id': order_id,
                                        'quantity': quantity,
                                        'sell_price': elem[0]
                                        })
                    self.pending['sell'][stock_name][elem[2]][3] -= quantity
                    quantity = 0
                    break
                elif quantity == quantity_sell:
                    transactions.append({
                                        'sell_order_id': elem[2],
                                        'buy_order_id': order_id,
                                        'quantity': quantity,
                                        'sell_price': elem[0]
                                        })
                    del self.pending['sell'][stock_name][elem[2]]
                    quantity = 0
                    break
                elif quantity > quantity_sell:
                    transactions.append({
                                        'sell_order_id': elem[2],
                                        'buy_order_id': order_id,
                                        'quantity': quantity_sell,
                                        'sell_price': elem[0]
                                        })
                    quantity -= quantity_sell
                    del self.pending['sell'][stock_name][elem[2]]

        if quantity:
            native_object['quantity'] = quantity
        else:
            native_object = {}

        return transactions, native_object

    def append_pending(self, native_object):
        stock_name = native_object['stock']
        action = native_object['action']

        if stock_name not in self.pending[action]:
            self.pending[action][stock_name] = {}

        self.pending[action][stock_name][native_object['order_id']] = [
                                                                        native_object['price'],
                                                                        native_object['timeval'],
                                                                        native_object['order_id'],
                                                                        native_object['quantity']
                                                                    ]




