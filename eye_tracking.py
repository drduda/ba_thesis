import numpy as np
import geometry
import ellipse_unprojection
import matplotlib.pyplot as plt
import json


class ProjectedPupil(geometry.Line):
    @staticmethod
    def construct_by_Double3DCircle(double_3d_circle, focal_length, visualize):
        FACTOR = 2
        pos_point = double_3d_circle.position + FACTOR * double_3d_circle.pos_orientation
        neg_point = double_3d_circle.position + FACTOR * double_3d_circle.neg_orientation

        pos_point = geometry.project_to_2d(pos_point, focal_length)
        neg_point = geometry.project_to_2d(neg_point, focal_length)
        position = geometry.project_to_2d(double_3d_circle.position, focal_length)

        if visualize:
            points = np.transpose([pos_point, neg_point])
            plt.plot(points[0], points[1], color='grey')
            plt.plot(position[0], position[1], marker='o', color='grey')

        return ProjectedPupil(position, pos_point - position)


def get_projected_center(ellipse_param_list, radius_3d_circle, focal_length, visualize=True):
    # Convert from JSON to list if necessary
    if type(ellipse_param_list) == str:
        ellipse_param_list = json.load(ellipse_param_list)

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
        projected_pupil = ProjectedPupil.construct_by_Double3DCircle(double_3d_circle, focal_length, visualize)
        projected_pupil_list.append(projected_pupil)
        pupil_list.append({"Double3DCircle": double_3d_circle})

    center = geometry.intersecting_lines(projected_pupil_list)
    if visualize:
        plt.plot(center[0], center[1], marker='x')
        plt.axis("equal")

    return center
