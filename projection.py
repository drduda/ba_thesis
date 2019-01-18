import numpy as np
import math
import matplotlib


class Eye:
    def __init__(self, center=np.array([0,0,0]), s_radius=1.0):
        self.center   = center
        self.s_radius = s_radius

    def rads_to_cartesians(self,rad_points):
        '''
             Neutral pos:: (long, lat, spherical_rad): (0,0,1) -> (0,1,0) in cartesian
             Spherical points are in regards to eye center which is considered for the recalculation
            :param rad_points: numpy array with shape (points size, 3)
            :return: cartesian numpy
         '''
        if rad_points.ndim == 1:
            raise TypeError("Nur Matritzen aus mehrere Punkte erlaubt!")
        else:
            if rad_points.shape[1] == 2:
                radius = self.s_radius
            else:
                radius = rad_points[:,2]
            hor = rad_points[:,0]; vert = rad_points[:,1];
            x = np.sin(hor) * np.cos(vert) * radius
            y = np.cos(hor) * np.cos(vert) * radius
            z = np.sin(vert) * radius
            return np.transpose([x,y,z])

class Pupil:
    def __init__(self, eye, spherical_deg):
        self.long_rad = spherical_deg[0]*180.0/math.pi
        self.lat_rad  = spherical_deg[1]*180.0/math.pi
        self.p_radius = spherical_deg[2]
        self.eye = eye

    def make_3d_circle(self, resolution = 100):
        '''
        :return: Cartesian 3D coordinates from pupil
        '''
        self.pupil_radius_rad = np.arcsin(self.p_radius/self.eye.s_radius)

        u = np.arange(0,math.pi*2,math.pi*2/resolution)
        long = np.cos(u)*self.pupil_radius_rad + self.long_rad
        lat  = np.sin(u)*self.pupil_radius_rad + self.lat_rad

        return self.eye.rads_to_cartesians(np.transpose([long,lat]))


