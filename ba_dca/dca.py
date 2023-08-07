from typing import Dict, Union
from binance.spot import Spot as Client
from binance.api import ClientError
from ba_dca.order import Order


class DCA:
    """_summary_"""

    def __init__(
        self,
        client: Client = None,
        base_url: str = "https://testnet.binance.vision",
        api_key: str = "yn9sfYQ4mzErFvJ7p1NQF2JGw7qiDBrBJq7bltyM6glJVAgZJ9VWre3z5p3Rs3dJ",
        api_secret: str = "o2ovcoCUu8aXs7KFBD43thJcrQPrlzY9TXuCxoAjzLAZv8KdPTEg6beXVbXeMiHb",
    ) -> None:
        self._client = (
            client
            if client
            else Client(base_url=base_url, api_key=api_key, api_secret=api_secret)
        )
        try:
            _ = self._client.account()
        except ClientError as error:
            raise RuntimeError("Couldn't create binance client") from error
        self._active_orders: Dict[int, Order] = {}
        self._new_order_id: int = 0
        self._next_order: Order = None
        self._next_order_id: int = 0
        self._symbols_precession: Dict[str, int] = {}
        self._build_symbols_precession()

    def balance(self) -> Union[Dict[str, float], None]:
        """Get the account balances as dict of [Coin_Name,Balance]

        Returns:
            Union[Dict[str, float], None]: Account balance as dict of [Coin_Name,Balance] or none.
        """
        account_info = self._client.account()
        if "balances" not in account_info:
            return None
        balances = account_info["balances"]
        balances_dict = {}
        for balance in balances:
            balances_dict[balance["asset"]] = float(balance["free"])
        return balances_dict

    def add_order(self, order: Order) -> int:
        """Add a new order to the active orders list.

        Args:
            order (Order): New order.

        Returns:
            int: Order id in the active orders list.
        """
        if order.symbol not in self._symbols_precession:
            raise RuntimeError(
                f"Symbol {order.symbol} not available for trading on Binance."
            )
        self._active_orders[self._new_order_id] = order
        self._new_order_id += 1
        self._update_next_order()
        return self._new_order_id - 1

    def _update_next_order(self):
        if not self._next_order:
            self._next_order = self._active_orders[self._new_order_id - 1]
        for order_id, order in self._active_orders.items():
            if order.next_execution_time < self._next_order.next_execution_time:
                self._next_order = self._active_orders[order_id]
                self._next_order_id = order_id

    @property
    def next_order(self) -> Order:
        """Return the next order to be executed.

        Returns:
            Order: Order to be executed next.
        """
        return self._next_order

    def _build_symbols_precession(self):
        for symbol_info in self._client.exchange_info()["symbols"]:
            self._symbols_precession[symbol_info["symbol"]] = int(
                symbol_info["quotePrecision"]
            )

    def _execute_next(self) -> int:
        quantity = round(
            self.next_order.amount, self._symbols_precession[self.next_order.symbol]
        )
        params = {
            "symbol": self.next_order.symbol,
            "side": "BUY",
            "type": "MARKET",
            "quoteOrderQty": quantity,
        }
        round(
            quantity,
        )
        try:
            response = self._client.new_order(**params)
        except ClientError as error:
            raise RuntimeError(
                f"Couldn't execute market order for pair {self.next_order.symbol}"
                f" quantity {quantity} {error.error_message}"
            ) from error
        print(response["fills"])
        self.next_order.execute()
        executed_order_id = self._next_order_id
        self._update_next_order()
        return executed_order_id

    def force_execute(self) -> int:
        """Force execute next order even if its not the time.

        Returns:
            int: Executed order id.
        """
        return self._execute_next()
