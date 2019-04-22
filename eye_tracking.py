import numpy as np
import geometry
import ellipse_unprojection


class ProjectedPupil(geometry.DoubleCircle):
    @staticmethod
    def construct_by_Double3DCircle(double_3d_circle):
        pass

def run(ellipse_param_list, radius_3d_circle, focal_length):
    """
    :param ellipse_param_list: list with dictionary of ellipse interface
    :return: dictionary with results
    """
    pupil_list = []
    for ellipse_dict in ellipse_param_list:
        double_3d_circle = ellipse_unprojection.Double3DCircle.constructByParamEllipse(
                                ellipse_dict["x_center"],
                                ellipse_dict["y_center"],
                                ellipse_dict["maj"],
                                ellipse_dict["min"],
                                ellipse_dict["rot"],
                                radius_3d_circle, focal_length)
        projected_pupil = ProjectedPupil.construct_by_Double3DCircle(double_3d_circle)
        pupil_list.append({"Double3dCircle": double_3d_circle,
                           "ProjectedPupil": projected_pupil})
