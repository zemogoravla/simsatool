# sunpos.py
# Get the sun position for a certain location and date-time
# https://levelup.gitconnected.com/python-sun-position-for-solar-energy-and-research-7a4ead801777
# AUTHOR: John Clark Craig  
# https://jccraig.medium.com/
# 
# The location of the Sun is expressed in terms of azimuth and elevation. 
# For clarity, let me define exactly what this means. Azimuth is the number of degrees 
# around on the horizon rotating east from north. So, if the Sun were located exactly 
# above the east horizon, its azimuth would be 90 degrees. At solar noon, when the Sun 
# crosses the sky due south of an observer (northern hemisphere case), its azimuth is 180 degrees. 
# The azimuth is expressed as a positive number of degrees ranging from 0 to 360.
# 
# Elevation is the number of degrees up from the horizon to the location of the center 
# of the Sun’s disk. When crossing the horizon, the Sun is at 0 degrees elevation, and when 
# the Sun is straight up, overhead at what’s called the zenith, its elevation angle is 90 degrees.


# --------------------------------------------------------------------------
# Alternative software: SUNCALC: https://github.com/kylebarron/suncalc-py
# Note: 
# Differences w.r.t. sunpos:
# a) returns angles in radians 
# b) uses a different azimuth orientation (direction along the horizon, 
#    measured from south to west), e.g. 0 is south and Math.PI * 3/4 is northwest
# --------------------------------------------------------------------------

import math
import datetime
def sunpos(when, location, refraction=False):
    """Get the sun position for a certain location and date-time
    https://levelup.gitconnected.com/python-sun-position-for-solar-energy-and-research-7a4ead801777
    AUTHOR: John Clark Craig  
    https://jccraig.medium.com/

    Args:
        when (UTC datetime or (year, month, day, hour, minute, second, timezone) tuple): Date-time instant 
        location ((latitude, longitude) tuple): Location 
        refraction (boolean): Take into account refraction. Defaults to False.

    Returns:
        double: azimuth in degrees
        double: elevation in degrees
    """
    # Extract the passed data
    if isinstance(when, datetime.datetime):
        when = (when.year, when.month, when.day, when.hour, when.minute, when.second, 0) #MUST BE UTC 

    year, month, day, hour, minute, second, timezone = when
    latitude, longitude = location
    # Math typing shortcuts
    rad, deg = math.radians, math.degrees
    sin, cos, tan = math.sin, math.cos, math.tan
    asin, atan2 = math.asin, math.atan2
    # Convert latitude and longitude to radians
    rlat = rad(latitude)
    rlon = rad(longitude)
    # Decimal hour of the day at Greenwich
    greenwichtime = hour - timezone + minute / 60 + second / 3600
    # Days from J2000, accurate from 1901 to 2099
    daynum = (
        367 * year
        - 7 * (year + (month + 9) // 12) // 4
        + 275 * month // 9
        + day
        - 730531.5
        + greenwichtime / 24
    )
    # Mean longitude of the sun
    mean_long = daynum * 0.01720279239 + 4.894967873
    # Mean anomaly of the Sun
    mean_anom = daynum * 0.01720197034 + 6.240040768
    # Ecliptic longitude of the sun
    eclip_long = (
        mean_long
        + 0.03342305518 * sin(mean_anom)
        + 0.0003490658504 * sin(2 * mean_anom)
    )
    # Obliquity of the ecliptic
    obliquity = 0.4090877234 - 0.000000006981317008 * daynum
    # Right ascension of the sun
    rasc = atan2(cos(obliquity) * sin(eclip_long), cos(eclip_long))
    # Declination of the sun
    decl = asin(sin(obliquity) * sin(eclip_long))
    # Local sidereal time
    sidereal = 4.894961213 + 6.300388099 * daynum + rlon
    # Hour angle of the sun
    hour_ang = sidereal - rasc
    # Local elevation of the sun
    elevation = asin(sin(decl) * sin(rlat) + cos(decl) * cos(rlat) * cos(hour_ang))
    # Local azimuth of the sun
    azimuth = atan2(
        -cos(decl) * cos(rlat) * sin(hour_ang),
        sin(decl) - sin(rlat) * sin(elevation),
    )
    # Convert azimuth and elevation to degrees
    azimuth = into_range(deg(azimuth), 0, 360)
    elevation = into_range(deg(elevation), -180, 180)
    # Refraction correction (optional)
    if refraction:
        targ = rad((elevation + (10.3 / (elevation + 5.11))))
        elevation += (1.02 / tan(targ)) / 60
    
    # Return azimuth and elevation in degrees
    return (round(azimuth, 2), round(elevation, 2))
    
def into_range(x, range_min, range_max):
    shiftedx = x - range_min
    delta = range_max - range_min
    return (((shiftedx % delta) + delta) % delta) + range_min
    
if __name__ == "__main__":
    import numpy as np

    # Close Encounters latitude, longitude
    location = (40.602778, -104.741667)
    # Fourth of July, 2022 at 11:20 am MDT (-6 hours)
    when = (2022, 7, 4, 11, 20, 0, -6)
    # Get the Sun's apparent location in the sky
    azimuth, elevation = sunpos(when, location, False)
    # Output the results
    print("\nWhen: ", when)
    print("Where: ", location)
    print("Azimuth: ", azimuth, np.deg2rad(azimuth))
    print("Elevation: ", elevation, np. deg2rad(elevation))
    
    # Expected result
    # When:  (2022, 7, 4, 11, 20, 0, -6)
    # Where:  (40.602778, -104.741667)
    # Azimuth:  121.38
    # Elevation:  61.91

    #-------------------------------------------------------------

    # TRY SUNCALC (must install first)--------------
    # Returns an object with the following properties:
    # altitude: sun altitude above the horizon in radians, e.g. 0 at the horizon and PI/2 at the zenith (straight over your head)
    # azimuth: sun azimuth in radians (direction along the horizon, measured from south to west), e.g. 0 is south and Math.PI * 3/4 is northwest

    # from suncalc import get_position, get_times
    # from datetime import datetime
    # import numpy as np

    # datetime_when = datetime.fromisoformat('{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}{:+03d}:00'.format(*when))
    # lon = location[1]
    # lat = location[0]
    # pos = get_position(datetime_when, lon, lat)
    # print(datetime_when)
    # print(pos)
    # print('suncalc azimuth =', (np.rad2deg(pos['azimuth']) + 180) % 360)
    # print('suncalc altitude =', np.rad2deg(pos['altitude']))
    #-------------------------------------------------

