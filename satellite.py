import numpy as np
import json


class Satellite():
    """Represents a Satellite in the Simulator. Holds the main properties of a satellite
    """
    def __init__(self, 
                 name = 'WorldView',
                 orbit_altitude_in_km = 617,
                 resolution_pixels_per_meter = 3.193):
        self.name = name
        self.orbit_altitude_in_km = orbit_altitude_in_km
        self.resolution_pixels_per_meter = resolution_pixels_per_meter
        
        
    def __str__(self):
        s = f'Satellite: {self.name}\n'
        s+= f'altitude (km): {self.orbit_altitude_in_km:.1f}\n'
        s+= f'resolution (pixels/m): {self.resolution_pixels_per_meter:.3f}'
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
        s = Satellite(c['name'], 
                      c['orbit_altitude_in_km'], 
                      c['resolution_pixels_per_meter'])
        return s
        
    
    def distance_relative_to_orbit_altitude(self, view_zenith_in_degrees):
        """Computes the (relative) distance of the satellite to the scene with respect 
           to orbit_altitude

        Args:
            view_zenith_in_degrees (float): zenith angle of the view

        Returns:
            float: satellite_distance / orbit_altitude
        """
        
        R = 6371  #earth radius in km
        d0 = self.orbit_altitude_in_km # distance for nadir view in km
        
        cos_ze = np.cos(np.radians(view_zenith_in_degrees))
        
        d1 = (-2*R*cos_ze + np.sqrt(4 * R**2 * cos_ze**2 + 4*(d0**2+2*R*d0))) / 2
        
        return d1/d0

        
    def view_pixels_per_meter(self, view_zenith_in_degrees):
        """Gets the resolution of a view taking into account the zenith angle

        Parameters
        ----------
        view_zenith_in_degrees : float  [0,90)
            Zenith angle of the view

        Returns
        -------
        float
            Resolution in pixels per meter 
        """        
         
        zoom_factor = 1 / self.distance_relative_to_orbit_altitude(view_zenith_in_degrees)

        return self.resolution_pixels_per_meter * zoom_factor
    








