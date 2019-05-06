import numpy as np
import geometry
import ellipse_unprojection



class ProjectedPupil(geometry.DoubleCircle):
    @staticmethod
    def construct_by_Double3DCircle(double_3d_circle, focal_length):
        FACTOR = 1
        pos_point = double_3d_circle.position + FACTOR * double_3d_circle.pos_orientation
        neg_point = double_3d_circle.position + FACTOR * double_3d_circle.neg_orientation

        pos_point = geometry.project_to_2d(pos_point, focal_length)
        neg_point = geometry.project_to_2d(neg_point, focal_length)
        pass


def run(ellipse_param_list, radius_3d_circle, focal_length):
    pupil_list = []
    for ellipse_dict in ellipse_param_list:
        double_3d_circle = ellipse_unprojection.Double3DCircle.constructByParamEllipse(
                                ellipse_dict["x_center"],
                                ellipse_dict["y_center"],
                                ellipse_dict["maj"],
                                ellipse_dict["min"],
                                ellipse_dict["rot"],
                                radius_3d_circle, focal_length)
        projected_pupil = ProjectedPupil.construct_by_Double3DCircle(double_3d_circle, focal_length)
        pupil_list.append({"Double3DCircle": double_3d_circle,
                           "ProjectedPupil": projected_pupil})
