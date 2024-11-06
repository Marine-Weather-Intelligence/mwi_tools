"""
    Calculation functions for coordinates
    - get_dist_ortho(pos1, pos2)
    - get_speed(pos1,pos2, dt)
    - get_heading(pos1, pos2)
    
"""
import math as m
import math

# Constant to used for WGS84
# consistent with PostGis
EARTH_RADIUS = 6371.0087714150598

# Constants for WGS-84 ellipsoid
WGS84_A = 6378137.0       # semi-major axis (meters)
WGS84_F = 1 / 298.257223563  # flattening
WGS84_B = WGS84_A * (1 - WGS84_F)  # semi-minor axis

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

def get_heading(pos1:tuple[float, float], pos2:tuple[float, float], n_digits = 0, method = 'spherical_azimuth') -> float: 
    """Calculate mean orthodromic heading between two positions

    Args:
        pos1 (tuple[float, float]): Tuple of (lat, lon) of pos1 in deg.dec
        pos2 (tuple[float, float]): Tuple of (lat, lon) of pos2 in deg.dec
        
    Returns:
        float: heading in degrees, normalized to [0-360]
    
    Example:
    >>> paris = (48.8566, 2.3522)
    >>> nyc = (40.7128, -74.0060)
    >>> get_heading(paris, nyc, 2)
    291.79
    >>> get_heading((-62.568, 178.948), (-62.562, -178.924))
    91 # Prime meridian crossing, should be 91
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = (m.radians(coord) for coord in pos1)
    lat2, lon2 = (m.radians(coord) for coord in pos2)

    azimuth = None

    if method == 'spherical_azimuth':
        azimuth = spherical_azimuth(lat1, lon1, lat2, lon2)
    elif method == 'normal_section_azimuth':
        azimuth = normal_section_azimuth(lat1, lon1, lat2, lon2)
    elif method == 'vincenty_azimuth':
        azimuth = vincenty_azimuth(lat1, lon1, lat2, lon2)
    else:
        azimuth = spherical_azimuth(lat1, lon1, lat2, lon2)
    
    # Convert azimuth from radians to degrees
    azimuth_deg = math.degrees(azimuth)

    # Normalize azimuth to [0, 360] degrees
    if azimuth_deg < 0:
        azimuth_deg += 360
    
    return round(azimuth_deg, n_digits) if n_digits > 0 else round(azimuth_deg)


def spherical_azimuth(lat1, lon1, lat2, lon2):
    """
    Spherical Azimuth. 
    Simplest, least accurate, fast. 
    Assumes Earth is a perfect sphere.

    Args:
        - lat1:float latitude of origin (radians)
        - lon1:float longitude of origin (radians)
        - lat2:float latitude of target (radians)
        - lon2:float longitude of target (radians)
    Returns:
        float: spherical_azimuth in radians
    """

    # Compute azimuth on spherical model
    delta_lon = lon2 - lon1
    numerator = math.sin(delta_lon) * math.cos(lat2)
    denominator = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
    
    # Azimuth in radians
    azimuth = math.atan2(numerator, denominator)
    
    return azimuth

def normal_section_azimuth(lat1, lon1, lat2, lon2):
    """
    More accurate, still fast, and accounts for Earth’s flattening but does not iterate.
    
    Args:
        - lat1:float latitude of origin (radians)
        - lon1:float longitude of origin (radians)
        - lat2:float latitude of target (radians)
        - lon2:float longitude of target (radians)
    Returns:
        float: normal_section_azimuth in radians
    """
    # Flattening and ellipsoid constants
    f = WGS84_F
    
    # Reduced latitude (using flattening)
    u1 = math.atan((1 - f) * math.tan(lat1))
    u2 = math.atan((1 - f) * math.tan(lat2))
    
    # Difference in longitudes
    delta_lambda = lon2 - lon1
    
    # Calculate trigonometric components
    sin_u1 = math.sin(u1)
    cos_u1 = math.cos(u1)
    sin_u2 = math.sin(u2)
    cos_u2 = math.cos(u2)
    
    sin_delta_lambda = math.sin(delta_lambda)
    cos_delta_lambda = math.cos(delta_lambda)
    
    # Calculate azimuth using normal-section approximation
    numerator = sin_delta_lambda * cos_u2
    denominator = cos_u1 * sin_u2 - sin_u1 * cos_u2 * cos_delta_lambda
    
    # Azimuth in radians
    azimuth = math.atan2(numerator, denominator)
    
    return azimuth


def vincenty_azimuth(lat1, lon1, lat2, lon2):
    """
    Spheroid Azimuth ; iterative Vincenty algorithm
    Most accurate, computationally intensive, iterative method that provides highly precise azimuths, especially for long distances or near the poles.
    Seems to be reference in PostGIS
    - https://fr.wikipedia.org/wiki/Formules_de_Vincenty
    - https://en.wikipedia.org/wiki/Vincenty%27s_formulae

    Yields the same result as ST_Azimuth, up to 6 decimals

    Args:
        - lat1:float latitude of origin (radians)
        - lon1:float longitude of origin (radians)
        - lat2:float latitude of target (radians)
        - lon2:float longitude of target (radians)
    Returns:
        float: spherical_azimuth in radians
    """
    # Flattening and ellipsoid constants
    f = WGS84_F
    
    # Reduced latitude (also called the parametric latitude), using tan reduction
    u1 = math.atan((1 - f) * math.tan(lat1))
    u2 = math.atan((1 - f) * math.tan(lat2))
    
    # Cosines and sines of reduced latitudes
    cos_u1 = math.cos(u1)
    sin_u1 = math.sin(u1)
    cos_u2 = math.cos(u2)
    sin_u2 = math.sin(u2)
    
    # Difference in longitudes
    lambda_diff = lon2 - lon1
    omega = lambda_diff  # Initial value of lambda for iteration
    
    # Iterate until lambda converges (Vincenty's formula is iterative)
    iter_limit = 1000
    for _ in range(iter_limit):
        sin_lambda = math.sin(lambda_diff)
        cos_lambda = math.cos(lambda_diff)
        
        sin_sigma = math.sqrt(
            (cos_u2 * sin_lambda) ** 2 +
            (cos_u1 * sin_u2 - sin_u1 * cos_u2 * cos_lambda) ** 2
        )
        if sin_sigma == 0:
            return 0  # coincident points
        
        cos_sigma = sin_u1 * sin_u2 + cos_u1 * cos_u2 * cos_lambda
        sigma = math.atan2(sin_sigma, cos_sigma)
        
        sin_alpha = cos_u1 * cos_u2 * sin_lambda / sin_sigma
        cos_alphasq = 1 - sin_alpha ** 2
        
        # Numerical stability for cos2_sigma_m
        cos2_sigma_m = cos_sigma - 2 * sin_u1 * sin_u2 / cos_alphasq if cos_alphasq != 0 else 0
        
        C = f / 16 * cos_alphasq * (4 + f * (4 - 3 * cos_alphasq))
        
        lambda_prev = lambda_diff
        lambda_diff = omega + (1 - C) * f * sin_alpha * (
            sigma + C * sin_sigma * (cos2_sigma_m + C * cos_sigma * (-1 + 2 * cos2_sigma_m ** 2))
        )
        
        # Check for convergence
        if abs(lambda_diff - lambda_prev) < 1e-12:
            break
    else:
        raise RuntimeError("Vincenty formula failed to converge")
    
    # Compute azimuth (initial bearing)
    azimuth = math.atan2(cos_u2 * math.sin(lambda_diff),
                         cos_u1 * sin_u2 - sin_u1 * cos_u2 * math.cos(lambda_diff))
    
    return azimuth
