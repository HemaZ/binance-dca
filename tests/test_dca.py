import unittest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ba_dca.dca import DCA
from ba_dca.order import Frequency, Order


class DCAUTests(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """

    def test_ctor_no_clinet(self):
        """_summary_"""
        with self.assertRaises(RuntimeError):
            _ = DCA(api_key="wrong")

    def test_balances(self):
        """_summary_"""
        cli = DCA()
        self.assertIsInstance(cli.balance(), dict)

    def test_adding_order(self):
        """_summary_"""
        dca = DCA()
        # Create Two orders
        order1 = Order("BTCUSDT", 0.01, Frequency.MONTHLY)
        order2 = Order("ETHUSDT", 0.01, Frequency.WEEKLY)
        dca.add_order(order1)
        dca.add_order(order2)
        # ETH order should be the next one
        self.assertEqual(dca.next_order.symbol, order2.symbol)
        # Adding a BNB order which should be earlier than ETH order
        order3 = Order("BNBUSDT", 0.01, Frequency.DAILY)
        dca.add_order(order3)
        self.assertEqual(dca.next_order.symbol, order3.symbol)
        # Adding an ADA order which should be later than BNB order
        order4 = Order("ADAUSDT", 0.01, Frequency.YEARLY)
        dca.add_order(order4)
        self.assertEqual(dca.next_order.symbol, order3.symbol)

    def test_force_execute(self):
        dca = DCA()
        # Create Two orders which has same start time, freq
        start_date = datetime.now()
        freq1 = relativedelta(seconds=+1)
        order1 = Order("BTCUSDT", 0.01, freq1, start_date)
        order2 = Order("ETHUSDT", 0.01, freq1, start_date)
        dca.add_order(order1)
        dca.add_order(order2)
        # Force executing next order should keep cycling between the two orders
        self.assertEqual(dca.next_order.symbol, order1.symbol)
        self.assertEqual(dca.force_execute(), 0)
        self.assertEqual(dca.next_order.symbol, order2.symbol)
        self.assertEqual(dca.force_execute(), 1)
        self.assertEqual(dca.next_order.symbol, order1.symbol)
        self.assertEqual(dca.force_execute(), 0)
