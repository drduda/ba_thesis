import numpy as np
import math
import cv2 as cv

"""
xz plane ist standard bis jetzt
"""

#TODO FOCAL LENGTH?
#TODO RIGHT HANDED COORDINATE SYSTEM?

class Eye:
    def __init__(self, center, sphere_radius):
        '''
        Angaben entprechen cm.
        :param center:
        :param sphere_radius:
        '''
        if center[1] + sphere_radius > -1:
            raise ValueError("Eyeball muss weiter nach hinten auf der y-Achse verschoben werden, sonst nicht von Kamera erfasst")
        else:
            self.center   = center
            self.sphere_radius = sphere_radius
            self.display_distance = round(self.center[1]+self.sphere_radius)/2 #Should be negative!

    def spherical_to_cartesians(self,spherical_points):
        '''
             Neutral pos:: (long, lat, spherical_rad): (0,0,1) -> (0,1,0) in cartesian
             Spherical points are in regards to eye center which is considered for the recalculation
            :param spherical_points: numpy array with shape (points size, 3)
            :return: cartesian numpy
         '''


        if spherical_points.shape[0] == 2:
            radius = self.sphere_radius
        else:
            radius = spherical_points[2]
        hor = spherical_points[0]; vert = spherical_points[1];
        x = np.sin(hor) * np.cos(vert) * radius + self.center[0]
        y = np.cos(hor) * np.cos(vert) * radius + self.center[1]
        z = np.sin(vert) * radius + self.center[2]
        return np.array([x,y,z])

    def project_to_2d(self, points_3d):
        if self.display_distance > 0:
            raise ValueError("Should be negative")
        '''
        Takes roughly half the distance of sphere surface and origin
        :param points_3d: cartesian points numpy array with shape(amount of points, 3)
        :return: 2d numpy array with shape(amount of points, 2)
        '''
        near = self.display_distance
        flat_x = points_3d[0]*near/points_3d[1]
        flat_z = points_3d[2]*near/points_3d[1]

        return np.array([flat_x, flat_z])

    def project_sphere(self, resolution = 50):
        raise NotImplementedError('Need to be restructured for new data structure')

        # draw sphere
        long = np.arange(0,math.pi*2,math.pi*2/resolution)
        lat = np.arange(0,math.pi*2,math.pi*2/resolution)

        grid = np.empty((long.size * lat.size,2))
        for i in range(0,long.size):
            for j in range(0, lat.size):
                grid[i*long.size + j][0] = long[i]
                grid[i * long.size + j][1] = lat[j]


        sphere = self.rads_to_cartesians(grid)
        return self.project_to_2d(sphere)


class Pupil:
    def __init__(self, eye, spherical_deg, resolution):
        """
        :param eye:
        :param spherical_deg: [long, lat, pupil_radius]
        :param resolution:
        """
        self.long_rad = math.radians(spherical_deg[0])
        self.lat_rad = math.radians(spherical_deg[1])
        self.pupil_radius = spherical_deg[2]
        self.eye = eye
        self.circle_points_spherical = self.make_3d_circle(resolution)
        self.circle_points_cart = self.eye.spherical_to_cartesians(self.circle_points_spherical)
        self.pupil_center_cart = self.eye.spherical_to_cartesians(np.array([self.long_rad, self.lat_rad]))
        self.ellipse = Ellipse(self.eye.project_to_2d(self.circle_points_cart))

    def make_3d_circle(self, resolution):
        '''
        :return: Cartesian 3D coordinates from pupil
        '''
        self.pupil_radius_rad = np.arcsin(self.pupil_radius/self.eye.sphere_radius)

        u = np.arange(0,math.pi*2,math.pi*2/resolution)
        long = np.cos(u)*self.pupil_radius_rad + self.long_rad
        lat = np.sin(u)*self.pupil_radius_rad + self.lat_rad

        return np.array([long, lat])

    def get_ellipse_param_dict(self):
        return {"x_center": self.ellipse.x_center,
                "y_center": self.ellipse.y_center,
                "maj": self.ellipse.major,
                "min": self.ellipse.minor,
                "rot": self.ellipse.anti_clockwise_rot}


class Ellipse:
    def __init__(self, points_on_ellipse):
        self.points_on_ellipse_T = np.transpose(points_on_ellipse)
        ellipse_cv = self.get_ellipse_param(self.points_on_ellipse_T)
        #TODO check if interface is correct
        self.x_center = ellipse_cv[0][0]
        self.y_center = ellipse_cv[0][1]
        self.major  = ellipse_cv[1][1]
        self.minor  = ellipse_cv[1][0]
        self.anti_clockwise_rot = ellipse_cv[2]

    @staticmethod
    def get_ellipse_param(points_2d):
        '''
        ellipse_cv has following parameters:
        center(x,y), (major_axis, minor_axis), anti_clockwise_rotation, 0, 360, color=255, line_thickness
        :param points_2d TRAVERSED
        :return:
        '''
        if points_2d.shape[0] == 3:
            raise TypeError("Nimmt nur traversierte np arrays an")
        #TODO check if interface is correct
        ellipse_cv = cv.fitEllipse(points_2d.astype(np.float32))
        return ellipse_cv
