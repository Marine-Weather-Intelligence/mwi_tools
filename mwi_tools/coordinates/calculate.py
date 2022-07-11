import math as m

def get_dist_ortho(pos1:list[float], pos2:list[float]) -> float: 
    """Calculate orthodromic distance between two points

    Args:
        pos1 (list[float]): List of lat and lon of pos1 in deg.dec
        pos2 (list[float]): List of lat and lon of pos2 in deg.dec

    Returns:
        float: Distance in m
    """
    lat1 = m.radians(pos1[0])
    lon1 = m.radians(pos1[1])
    lat2 = m.radians(pos2[0])
    lon2 = m.radians(pos2[1])

    #Case of same position 
    if (lat1 == lat2 and lon1 == lon2) : 
        return 0

    B = m.acos(m.sin(lat1)*m.sin(lat2)+m.cos(lat1)*m.cos(lat2)*m.cos(abs(lon1-lon2)))
    return B*12735.3/2*1000;

def get_speed(pos1:list[float], pos2:list[float], dt:int) -> float : 
    """Calculate mean speed in knots between two positions

    Args:
        pos1 (list[float]): List of lat and lon of pos1 in deg.dec
        pos2 (list[float]): List of lat and lon of pos2 in deg.dec
        dt (int): delta time in sec between the two positions

    Returns:
        float: mean speed in knots between two points
    """
    dist = get_dist_ortho(pos1, pos2)
    v = dist/dt #speed m/s
    return round(v * 1.9438, 1)

def get_heading(pos1:list[float], pos2:list[float]) -> int: 
    """Calculate mean orthodromic heading between two positions

    Args:
        pos1 (list[float]): List of lat and lon of pos1 in deg.dec
        pos2 (list[float]): List of lat and lon of pos2 in deg.dec
        
    Returns:
        int: mean orthodromic heading between two points
    """
    lat1 = m.radians(pos1[0])
    lon1 = m.radians(pos1[1])
    lat2 = m.radians(pos2[0])
    lon2 = m.radians(pos2[1])

    #Case of same position 
    if (lat1 == lat2 and lon1 == lon2) : 
        return None
    B = m.acos(m.sin(lat1)*m.sin(lat2)+m.cos(lat1)*m.cos(lat2)*m.cos(abs(lon1-lon2)))

    #On a ici mis un round car cela faisait parfois moins que -1
    heading = m.acos(round((m.sin(lat2)-m.sin(lat1)*m.cos(B))/m.cos(lat1)/m.sin(B),6))
    heading = heading*180/m.pi
    if (lon2 <lon1) : 
        return round(360-heading)
    else : 
        return round(heading)