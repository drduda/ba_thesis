import numpy as np
import math
import cv2 as cv


class Eye:
    def __init__(self, center=np.array([0.0,-5.0,0.0]), s_radius=1.2):
        '''
        Angaben entprechen cm.
        :param center:
        :param s_radius:
        '''
        if center[1] + s_radius > -1:
            raise ValueError("Eyeball muss weiter nach hinten auf der y-Achse verschoben werden, sonst nicht von Kamera erfasst")
        else:
            self.center   = center
            self.s_radius = s_radius
            self.display_distance = round(self.center[1]+self.s_radius)/2 #Should be negative!

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
            x = np.sin(hor) * np.cos(vert) * radius + self.center[0]
            y = np.cos(hor) * np.cos(vert) * radius + self.center[1]
            z = np.sin(vert) * radius + self.center[2]
            return np.transpose([x,y,z])

class Pupil:
    def __init__(self, eye, spherical_deg, resolution = 100):
        self.long_rad = spherical_deg[0]*math.pi/180.0
        self.lat_rad  = spherical_deg[1]*math.pi/180.0
        self.p_radius = spherical_deg[2]
        self.eye = eye
        self.circle_points = self.make_3d_circle(resolution)
        self.ellipse_points = self.project_to_2d(eye, self.circle_points)
        self.ellipse_param = self.get_ellipse_param(self.ellipse_points)

    def make_3d_circle(self, resolution):
        '''
        :return: Cartesian 3D coordinates from pupil
        '''
        self.pupil_radius_rad = np.arcsin(self.p_radius/self.eye.s_radius)

        u = np.arange(0,math.pi*2,math.pi*2/resolution)
        long = np.cos(u)*self.pupil_radius_rad + self.long_rad
        lat  = np.sin(u)*self.pupil_radius_rad + self.lat_rad

        return self.eye.rads_to_cartesians(np.transpose([long,lat]))

    def project_to_2d(self, eye, points_3d):
        if eye.display_distance > 0:
            raise ValueError("Should be negative")
        '''
        Takes roughly half the distance of sphere surface and origin
        :param points_3d: cartesian points numpy array with shape(amount of points, 3)
        :return: 2d numpy array with shape(amount of points, 2)
        '''
        near = eye.display_distance
        flat_x = points_3d[:,0]*near/points_3d[:,1]
        flat_z = points_3d[:,2]*near/points_3d[:,1]

        return np.transpose([flat_x, flat_z])

    def get_ellipse_param(self, points_2d):
        '''
        center_points_has following parameters:
        center(x,y), (major_axis, minor_axis), anti_clockwise_rotation, 0, 360, color=255, line_thickness
        :param points_2d:
        :return:
        '''
        ellipse_cv = cv.fitEllipse(points_2d.astype(np.float32))
        #Trasnformed to np array
        return ellipse_cv
