from mwi_tools.coordinates import get_heading

lat1, lon1 = (48.8566, 2.3522)   # Position 2 (e.g., Paris)
lat2, lon2 = (40.7128, -74.0060)  # Position 1 (e.g., New York)

print(f"Spherical : {get_heading((lat1, lon1), (lat2, lon2), 4, 'spherical_azimuth')} degrees")
print(f"Normal section : {get_heading((lat1, lon1), (lat2, lon2), 4, 'normal_section_azimuth')} degrees")
print(f"Vincenty: {get_heading((lat1, lon1), (lat2, lon2), 4, 'vincenty_azimuth')} degrees")


lat1, lon1 = (-62.568, 178.948)
lat2, lon2 = (-62.562, -178.924)

print(f"Spherical : {get_heading((lat1, lon1), (lat2, lon2), 4, 'spherical_azimuth')} degrees")
print(f"Normal section : {get_heading((lat1, lon1), (lat2, lon2), 4, 'normal_section_azimuth')} degrees")
print(f"Vincenty: {get_heading((lat1, lon1), (lat2, lon2), 4, 'vincenty_azimuth')} degrees")

lat1, lon1 = (12.568, -0.01)
lat2, lon2 = (12.568, 0.01)

print(f"Spherical : {get_heading((lat1, lon1), (lat2, lon2), 4, 'spherical_azimuth')} degrees")
print(f"Normal section : {get_heading((lat1, lon1), (lat2, lon2), 4, 'normal_section_azimuth')} degrees")
print(f"Vincenty: {get_heading((lat1, lon1), (lat2, lon2), 4, 'vincenty_azimuth')} degrees")
