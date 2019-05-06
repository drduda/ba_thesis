import numpy as np
import geometry
import ellipse_unprojection



class ProjectedPupil(geometry.Line):
    @staticmethod
    def construct_by_Double3DCircle(double_3d_circle, focal_length):
        FACTOR = 1
        pos_point = double_3d_circle.position + FACTOR * double_3d_circle.pos_orientation

        pos_point = geometry.project_to_2d(pos_point, focal_length)
        position = geometry.project_to_2d(double_3d_circle.position, focal_length)

        return ProjectedPupil(position, pos_point - position)


def run(ellipse_param_list, radius_3d_circle, focal_length):
    pupil_list = []
    projected_pupil_list = []
    for ellipse_dict in ellipse_param_list:
        double_3d_circle = ellipse_unprojection.Double3DCircle.constructByParamEllipse(
                                ellipse_dict["x_center"],
                                ellipse_dict["y_center"],
                                ellipse_dict["maj"],
                                ellipse_dict["min"],
                                ellipse_dict["rot"],
                                radius_3d_circle, focal_length)
        projected_pupil = ProjectedPupil.construct_by_Double3DCircle(double_3d_circle, focal_length)
        projected_pupil_list.append(projected_pupil)
        pupil_list.append({"Double3DCircle": double_3d_circle})

    return geometry.intersecting_lines(projected_pupil_list)
