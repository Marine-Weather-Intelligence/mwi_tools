"""
    Calculation functions for coordinates
    - get_dist_ortho(pos1, pos2)
    - get_speed(pos1,pos2, dt)
    - get_heading(pos1, pos2)
    
"""
import math as m

# Constant to used for WGS84
# consistent with PostGis
EARTH_RADIUS = 6371.0087714150598

MS_TO_KNOTS = 3600 / 1852

def get_dist_ortho(pos1:tuple[float, float], pos2:tuple[float, float]) -> float: 
    """Calculate orthodromic distance between two points

    Args:
        pos1 (tuple[float, float]): Tuple (lat, lon) in deg.dec
        pos2 (tuple[float, float]): Tuple (lat, lon) in deg.dec

    Returns:
        float: Distance in m

    Example:
    >>> paris = (48.8566, 2.3522)
    >>> nyc = (40.7128, -74.0060)
    >>> print(get_dist_ortho(paris, nyc))
    5837248.940376267
    """
    lat1, lon1 = (m.radians(coord) for coord in pos1)
    lat2, lon2 = (m.radians(coord) for coord in pos2)

    #Case of same position 
    if (lat1 == lat2 and lon1 == lon2) : 
        return 0

    B = m.acos(m.sin(lat1)*m.sin(lat2)+m.cos(lat1)*m.cos(lat2)*m.cos(abs(lon1-lon2)))
    return B * EARTH_RADIUS * 1000

def get_speed(pos1:tuple[float, float], pos2:tuple[float, float], dt:int, n_digits:int = 1) -> float : 
    """Calculate mean speed in knots between two positions

    Args:
        pos1 (tuple[float, float]): Tuple of lat and lon of pos1 in deg.dec
        pos2 (tuple[float, float]): Tuple of lat and lon of pos2 in deg.dec
        dt (int): delta time in sec between the two positions

    Returns:
        float: mean speed in knots between two points
    Example:
    >>> quiberon = (47.475911695481756, -3.1208038330078125)
    >>> palais = (47.34696504890934, -3.1468963623046875)
    >>> get_speed(quiberon, palais, 3600)
    7.8
    >>> get_speed(quiberon, palais, 3600, 2)
    7.81
    """
    dist = get_dist_ortho(pos1, pos2)
    v = dist/dt # speed m/s
    return round(v * MS_TO_KNOTS, n_digits)

def get_heading(pos1:list[float], pos2:list[float]) -> int: 
    """Calculate mean orthodromic heading between two positions

    Args:
        pos1 (list[float]): List of lat and lon of pos1 in deg.dec
        pos2 (list[float]): List of lat and lon of pos2 in deg.dec
        
    Returns:
        int: mean orthodromic heading between two points
    """
    lat1 = m.radians(pos1[0])
    #print("lat1 : "+ str(pos1[0])+"°"+str(lat1)+"rad")
    lon1 = m.radians(pos1[1])
    #print("lon1 : "+ str(pos1[1])+"°"+str(lon1)+"rad")
    lat2 = m.radians(pos2[0])
    #print("lat2 : "+ str(pos2[0])+"°"+str(lat2)+"rad")
    lon2 = m.radians(pos2[1])
    #print("lon2 : "+ str(pos2[1])+"°"+str(lon2)+"rad")

    #Case of same position 
    if (lat1 == lat2 and lon1 == lon2) : 
        return None
    B = m.acos(m.sin(lat1)*m.sin(lat2)+m.cos(lat1)*m.cos(lat2)*m.cos(abs(lon1-lon2)))

    #On a ici mis un if car cela faisait parfois moins que -1 ou plus que 1
    temp = (m.sin(lat2)-m.sin(lat1)*m.cos(B))/m.cos(lat1)/m.sin(B)
    if temp < -1 : 
        temp = -1
    elif temp > 1 : 
        temp =1
    heading = m.acos(temp)
    heading = heading*180/m.pi
    if (lon2 <lon1) : 
        return round(360-heading)
    else : 
        return round(heading)