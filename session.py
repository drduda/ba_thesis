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
            return p.ellipse
        else:
            raise StopIteration


class Session(Iterator):
    def __init__(self, pupil_param_list: list, eye_center, sphere_radius, resolution, radius_3d_circle):
        """

                :param pupil_param_list: for example [[long, lat, pupil_radius],...]
                :param eye_center: np.array([x, y, z])
                :param sphere_radius: float of radius of the eyeball measured in centimeter
                :param resolution: how many coordinates are used to track the ellipse
                """
        projectionSession = iter(ProjectionSession(pupil_param_list, eye_center, sphere_radius, resolution))
        unprojectionSession = iter(UnprojectionSession(projectionSession, radius_3d_circle))

class UnprojectionSession(Iterator):
    def __init__(self, tracked_ellipses_iterator, radius_3d_circle):
        self.three_dimensional_circle_list = []
        for ellipse in tracked_ellipses_iterator:
            three_dimensional_circle = ellipse_unprojection.Double3DCircle.constructByParamEllipse(
                ellipse.x_center, ellipse.y_center, ellipse.major, ellipse.minor, ellipse.anti_clockwise_rot, radius_3d_circle)
            #TODO FOCAL LENGTH
            self.three_dimensional_circle_list.append(three_dimensional_circle)

    def __next__(self):
        pass
