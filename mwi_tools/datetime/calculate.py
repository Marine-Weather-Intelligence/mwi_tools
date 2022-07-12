"""
    Calculating functions for datetime:
    - round_datetime(datetime)
    - get_delta(datetime1, datetime2)
"""

import datetime
from datetime import timedelta

def round_datetime(datetime : datetime) -> datetime: 
    """Get the closest datetime hour with minutes = 0

    Args:
        datetime (datetime): Datetime object

    Returns:
        datetime: Datetime object rounded
    """

    return (datetime.replace(second=0, microsecond=0, minute=0, hour=datetime.hour)+timedelta(hours=datetime.minute//30))

def get_delta(datetime1 : datetime, datetime2 : datetime) -> datetime: 
    """Get the time elapsed between two datetimes

    Args:
        datetime1 (datetime): Datetime object
        datetime2 (datetime): Datetime object

    Returns:
        datetime: Delta time
    """

    return (datetime2-datetime1)