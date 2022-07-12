"""
    Functions to deal with wind variables : 
    - get_TWS(u,v)
    - get_dir(u,v)
    - set_TWA(TWD, heading)

"""
import math as m

def get_TWS(u:float, v:float) -> float:
    """Calculate True Wind Speed from u and v component of wind in m/s

    Args:
        u (float): u component of wind in m/s
        v (float): v component of wind in m/s

    Returns:
        float: TWS in knots
    """
    return round(m.sqrt(u**2+v**2)*1.9438,1)

def get_dir(u:float, v:float) -> int:
    """Calculate wind direction in degrees from u and v component of wind in m/s

    Args:
        u (float): u component of wind in m/s
        v (float): v component of wind in m/s

    Returns:
        int: Wind direction in degrees
    """
    TWD = m.atan2(-u, -v)*180/m.pi
    if (TWD < 0) :
        return round(TWD +360)
    else :
        return round(TWD)

def set_TWA(TWD : int, heading : int) -> int:
    """Calculate TWA from TWD and Heading

    Args:
        TWD (int): TWD in deg
        heading (int): Heading in deg

    Returns:
        int: TWA in deg
    """
    TWA = TWD - heading
    if (TWA >180):
        return TWA -360
    elif (TWA < -180) :
        return TWA + 360
    else :
        return TWA