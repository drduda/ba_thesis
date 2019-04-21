"""
Module for all geometry classes and methods that are used in multiple modules
"""


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
