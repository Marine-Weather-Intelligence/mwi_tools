"""
    Formatting functions for datetime:
"""

import datetime

def format_date1(date :float) -> datetime.date : 
    """Convert a date (float) of type %y%m%d.0 to date object
    Ex : Traces TJV TRR  (20211125.0)

    Args:
        date (float): date of type %y%m%d.0 

    Returns:
        datetime.date : date object
    """

    date = str(int(date))
    day = date[-2:]
    month = date[4:6]
    year = date[:4]
    return datetime.date(int(year), int(month), int(day))

def format_date2(date:str) -> datetime.date : 
    """Convert a date (str) of type %d/%m/%Y to date object
    Ex : 25/11/2021

    Args:
        date (str): date of type %d/%m/%Y

    Returns:
        datetime.date : date object
    """

    return datetime.datetime.strptime(date, "%d/%m/%Y").date()

def format_date3(date:str) -> datetime.date : 
    """Convert a date (str) of type %m/%d/%y to date object
    Ex : 11/25/2021

    Args:
        date (str): date of type %d/%m/%y

    Returns:
        datetime.date : date object
    """

    return datetime.datetime.strptime(date, "%m/%d/%y").date()

def format_time1(time : float) -> datetime.time :
    """Convert a time of type float like %h%min%sec.0 to time object
    Ex : 123000.0

    Args:
        time (float): time of type float like %h%min%sec.0

    Returns:
        datetime.time: time object
    """

    date = str(int(time))
    sec = date[-2:]
    if len(date) == 4: 
        m = date[0:2]
        h = '00'
    elif len(date) == 5:
        m = date[1:3]
        h = '0'+date[0]
    else : 
        m = date[2:4]
        h = date[:2]
    return datetime.time(int(h),int(m),int(sec))

def format_time2(time : str) -> datetime.time :
    """Convert a time of type str like %H:%M:%S to time object
    Ex : 12:30:00
    
    Args:
        time (str): time of type str like %H:%M:%S

    Returns:
        datetime.time: time object
    """
    return datetime.datetime.strptime(time, "%H:%M:%S").time()
