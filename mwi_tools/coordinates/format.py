def format_longitude180(lon : float) -> float :
    """Format a longitude of type %deg.%decimal between 0 and 360 to a longitude of type %deg.%decimal between -180 and 180.

    Args:
        lon (float): Longitude of type %deg.%decimal between 0 and 360. 

    Returns:
        float: Longitude of type %deg.%decimal between -180 and 180. 
    """
    
    if lon > 180 : 
        return lon-360
    else : 
        return lon

def rewrite_coord(coord : float) -> str : 
    """Convert a latitude or longitude of type %deg%min.%dec to type %deg°%min.%dec.
    Ex : 2901.3762 en -29°01.3762

    Args:
        coord (float): Latitude or longitude of type %deg%min.%dec

    Returns:
        str: Latitude or longitude of type %deg°%min.%dec
    """

    temp = str(coord).split('.')
    minutes = temp[0][-2:]
    minutes = minutes+'.'+temp[1]
    deg = temp[0][:-2]

    #If deg is 0, we had 0 to the str
    if (deg == '') or (deg =='-') : 
        deg = deg+'0'
    return deg+'°'+minutes

def convert_coord_to_degdec(coord: str) -> float : 
    """Convert coordinates of type %deg°%min.%dec to type %deg.%dec
    Ex : 50°40.35 --> 50.6725

    Args:
        coord (str): Latitude or longitude of type %deg°%min.%dec

    Returns:
        float: Latitude or longitude of type %deg.%dec
    """

    temp = coord.split('°')
    deg = int(float(temp[0]))
    decimal = round(float(temp[1])/60,6)
    if deg<0 : 
        return deg-decimal
    else : 
        return deg+decimal

def convert_coord_to_degdec2(coord: str) -> float : 
    """Convert coordinates of type %deg.%min%dec%N to type %deg.%dec
    Ex : 50.4035N --> 50.6725

    Args:
        coord (str): Latitude or longitude of type %deg.%min%dec%N

    Returns:
        float: Latitude or longitude of type %deg.%dec
    """
    letter = coord[-1]
    coord = coord[:-1]
    coord = float(coord)
    deg = int(coord)
    min = (coord - deg)*100
    decimal = min/60
    coord = round(deg+decimal,2)
    if letter == 'N' or letter == 'E' : 
        return coord
    else : 
        return -coord