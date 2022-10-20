
import json
import numpy as np

class Location():
    """Location manager.
    """
    def __init__(self, 
                 name = 'San Fernando',
                 aoi = {'coordinates': [[
                    [-58.58923437034032, -34.49059476958225], 
                    [-58.58923437034032, -34.4891885066768], 
                    [-58.58733243810684, -34.4891885066768], 
                    [-58.58733243810684, -34.49059476958225], 
                    [-58.58923437034032, -34.49059476958225]]], 
                    'type': 'Polygon'},
                 altitude_range = [-100, 100],
                 lon_lat_alt_origin=None):
        """Location manager

        Args:
            name (str, optional): Name of the location. Defaults to 'San Fernando'.
            aoi (GeoJSON polygon dict, optional): Area of interest. Defaults to {'coordinates': [[ [-58.58923437034032, -34.49059476958225], [-58.58923437034032, -34.4891885066768], [-58.58733243810684, -34.4891885066768], [-58.58733243810684, -34.49059476958225], [-58.58923437034032, -34.49059476958225]]], 'type': 'Polygon'}.
            altitude_range (list, optional): Min-max altitudes in meters. Defaults to [-100, 100].
            lon_lat_alt_origin (list), optional): Origin as [longitude, latitude, altitude] . Defaults to None.
        """

        self.name = name
        self.aoi = aoi
        self.altitude_range = altitude_range

        # if lon_lat_alt_origin was not given, set it as the VOI origin
        if lon_lat_alt_origin is None:
            lon, lat = self.aoi_lon_lat_center()
            self.lon_lat_alt_origin = [lon, lat, (altitude_range[0]+altitude_range[1])/2]
        else:
            self.lon_lat_alt_origin = lon_lat_alt_origin

    
    
    def __str__(self):
        s = f'Location: {self.name}\n'
        s+= f'aoi: {self.aoi}\n'
        s+= f'altitude_range(m): {self.altitude_range}\n'
        s+= f'Origin (lon, lat, alt): {self.lon_lat_alt_origin}'
        return(s)
    
    def to_json_file(self, json_filename):
        json_str = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        with open(json_filename,'w') as f:
            f.write(json_str)
            
    @staticmethod
    def from_json_file(json_filename):
        with open(json_filename, 'r') as f:
            c = json.loads(f.read())
            print(c)
        s = Location(c['name'], 
                      c['aoi'], 
                      c['altitude_range'],
                      c['lon_lat_alt_origin'])
        return s

    def aoi_lon_lat_center(self):
        coords = np.array(self.aoi['coordinates'][0])
        lons = coords[:,0]
        lats = coords[:,1]
        lon = (np.max(lons) + np.min(lons)) / 2
        lat = (np.max(lats) + np.min(lats)) / 2
        return lon, lat