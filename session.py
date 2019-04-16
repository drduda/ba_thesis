import numpy as np
import projection
import ellipse_unprojection


class Iterator:
    def __iter__(self):
        self.i = 0
        return self

class ProjectionSession(Iterator):
    """
    Iterator for the simulation/ generating of data
    """
    def __init__(self, pupil_param_list: list, eye_center, sphere_radius, resolution):
        """

        :param pupil_param_list: for example [[long, lat, pupil_radius],...]
        :param eye_center: np.array([x, y, z])
        :param sphere_radius: float of radius of the eyeball measured in centimeter
        :param resolution: how many coordinates are used to track the ellipse
        """
        self.eye = projection.Eye(eye_center, sphere_radius)
        self.gaze_amount = len(pupil_param_list)
        self.pupils = []
        for gaze_id in range(0, self.gaze_amount):
            p = projection.Pupil(self.eye, pupil_param_list[gaze_id], resolution)
            self.pupils.append(p)

    def __next__(self):
        if self.i < self.gaze_amount:
            p = self.pupils[self.i]
            self.i += 1
            return p
        else:
            raise StopIteration

