import re
from enum import Enum
from dateutil.relativedelta import relativedelta


class Frequency(Enum):
    """Trading frequency."""

    HOURLY = 1
    DAILY = 2
    WEEKLY = 3
    MONTHLY = 4
    YEARLY = 5

    @classmethod
    def freq_to_relative_delta(cls, freq: "Frequency") -> relativedelta:
        """Convert the Frequency enum to dateutil.relativedelta.

        Args:
            freq (Frequency): Order frequency as time.

        Returns:
            relativedelta: dateutil.relativedelta to be used with datetime module.
        """
        if freq == Frequency.HOURLY:
            return relativedelta(hours=+1)
        if freq == Frequency.DAILY:
            return relativedelta(days=+1)
        if freq == Frequency.WEEKLY:
            return relativedelta(weeks=+1)
        if freq == Frequency.MONTHLY:
            return relativedelta(months=+1)
        if freq == Frequency.YEARLY:
            return relativedelta(years=+1)
        return relativedelta


def str_to_relativedelta(text: str) -> relativedelta:
    """Convert string which represents relativedelta to a relativedelta object.

    Args:
        text (str): string which represents relativedelta.

    Returns:
        relativedelta: Converted relativedelta object.
    """
    # Define a pattern with a positive lookbehind for "years"
    pattern_years = r"(?<=years=)[+-]?\d+"
    pattern_months = r"(?<=months=)[+-]?\d+"
    pattern_weeks = r"(?<=weeks=)[+-]?\d+"
    pattern_days = r"(?<=days=)[+-]?\d+"
    pattern_hours = r"(?<=hours=)[+-]?\d+"
    pattern_minutes = r"(?<=minutes=)[+-]?\d+"
    pattern_seconds = r"(?<=seconds=)[+-]?\d+"

    # Find the number after "years" in the text
    match = re.search(pattern_years, text)
    if match:
        n_years = int(match.group())
    else:
        n_years = 0

    # Find the number after "years" in the text
    match = re.search(pattern_months, text)
    if match:
        n_months = int(match.group())
    else:
        n_months = 0

    # Find the number after "years" in the text
    match = re.search(pattern_weeks, text)
    if match:
        n_weeks = int(match.group())
    else:
        n_weeks = 0

    # Find the number after "years" in the text
    match = re.search(pattern_days, text)
    if match:
        n_days = int(match.group())
    else:
        n_days = 0

    # Find the number after "years" in the text
    match = re.search(pattern_hours, text)
    if match:
        n_hours = int(match.group())
    else:
        n_hours = 0

    # Find the number after "years" in the text
    match = re.search(pattern_minutes, text)
    if match:
        n_minutes = int(match.group())
    else:
        n_minutes = 0

    # Find the number after "years" in the text
    match = re.search(pattern_seconds, text)
    if match:
        n_seconds = int(match.group())
    else:
        n_seconds = 0

    return relativedelta(
        years=+n_years,
        months=+n_months,
        weeks=+n_weeks,
        days=+n_days,
        hours=+n_hours,
        minutes=+n_minutes,
        seconds=+n_seconds,
    )
