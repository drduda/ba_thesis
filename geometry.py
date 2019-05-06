"""
Module for all geometry classes and methods that are used in multiple modules
"""
import numpy as np


class DoubleCircle:
    def __init__(self, position, pos_orientation, neg_orientation):
        self.position = position
        self.pos_orientation = pos_orientation
        self.neg_orientation = neg_orientation
        self.sign = None

    def set_orientation(self, sign):
        """
        Sets the orientation in order to solve two-circle ambiguity
        :param sign: True for positive, False for negative
        """
        if self.sign is not None:
            raise PermissionError("Sign can only be set once")
        self.sign = sign

    @property
    def orientation(self):
        if self.sign is None:
            raise ValueError("True orientation is not set yet")
        if self.sign:
            return self.pos_orientation
        else:
            return self.neg_orientation


class ParametricEllipse:
    def __init__(self, x_center, y_center, maj, min, rot):
        if maj < min:
            raise ValueError("Major axis needs to be bigger than minor")
        if not (0 <= rot <= 180):
            raise ValueError("Not more than 180 degrees rotation possible")
        self.x_center = x_center
        self.y_center = y_center
        self.maj = maj
        self.min = min
        self.rot = rot


def project_to_2d(point_3d, focal_length, return_2d = True):
    """
    projected plane is xy
    :param point_3d: np.array([x,y,z])
    :param focal_length:
    :param return_2d: if True than 2d points will be returned,
    else as 3d elements on plane
    :return:
    """
    flat_x = focal_length*point_3d[0]/point_3d[2]
    flat_y = focal_length*point_3d[1]/point_3d[2]
    if return_2d:
        return np.array([flat_x, flat_y])
    else:
        return np.array([flat_x, flat_y, focal_length])


