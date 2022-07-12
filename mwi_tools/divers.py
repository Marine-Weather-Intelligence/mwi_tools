"""Diverse functions usefull for development purposes
"""

def x_round_25(x:float) -> float:
    """Round to the nearest 0.25 value

    Args:
        x (float): 

    Returns:
        float: rounded value
    """

    return round(x*4)/4

def x_round_50(x:float) -> float:
    """Round to the nearest 0.5 value

    Args:
        x (float): 

    Returns:
        float: rounded value
    """

    return round(x*2)/2