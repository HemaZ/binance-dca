"""BA DCA CLI"""
import logging as log
from enum import Enum
import typer
from ba_dca.dca import DCA
from ba_dca.order import Order, Frequency


class OrderFrequency(str, Enum):
    """Command line order freq."""

    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


def convert_freq(freq: OrderFrequency) -> Frequency:
    """Convert the command line frequency to the BA-DCA freq.

    Args:
        freq (OrderFrequency): Command line order freq.

    Returns:
        Frequency: BA-DCA Freq.
    """
    if freq == "hourly":
        return Frequency.HOURLY
    if freq == "daily":
        return Frequency.DAILY
    if freq == "weekly":
        return Frequency.WEEKLY
    if freq == "monthly":
        return Frequency.MONTHLY
    if freq == "yearly":
        return Frequency.YEARLY
    return None


dca = DCA()
app = typer.Typer()


@app.command()
def run(block: bool = True):
    """Run the orders.

    Args:
        block (bool, optional): Keep running and don't return. Defaults to True.
    """
    dca.run(block)


@app.command()
def new(symbol: str, amount: float, freq: OrderFrequency):
    """Create a new order

    Args:
        symbol (str): Order symbol.
        amount (float): order amount.
        freq (OrderFrequency): order frequency.
    """
    try:
        order1 = Order(symbol, amount, convert_freq(freq))
        dca.add_order(order1)
    except Exception as e:
        log.error(e)


if __name__ == "__main__":
    app()
