import projection
import numpy as np
import eye_tracking
import matplotlib.pyplot as plt
import pupil_param_lists


####PARAMETERS###
EYE_CENTER = np.array([0.0, -5.0, 0.0])
SPHERE_RADIUS = 1.2
RESOLUTION = 100
RADIUS_3D_CIRCLE = 4
PUPIL_PARAM_LIST = pupil_param_lists.symmetric_30_15
FOCAL_LENGTH = 1
PROJECTED_CENTER = [EYE_CENTER[0]/-EYE_CENTER[1], EYE_CENTER[2]/-EYE_CENTER[1]]


def simulate_input_data(pupil_param_list = PUPIL_PARAM_LIST):
    """
    Class that simulates an eye looking around and outputs the
    the recorded pupils in their 2D elliptic form
    All values in degrees or centimeters
    :param pupil_param_list: [[longitude, latitude, radius],..]
    :return: elliptic input data for the actual eye tracking
    """
    eye = projection.Eye(EYE_CENTER, SPHERE_RADIUS)
    ellipse_param_list = []
    for i in range(len(PUPIL_PARAM_LIST)):
        p = projection.Pupil(eye, PUPIL_PARAM_LIST[i], RESOLUTION)
        ellipse_param_list.append(p.get_ellipse_param_dict())
    return ellipse_param_list


def reprojection(input_data, visualize):
    """
    :param input_data: list of dictionaries, each dictionary represents an ellipse and looks like
        {"x_center", "y_center": , "maj": , "min", "rot": rotated major axis clockwise in degrees}
    :return: projected eye center np.array([x, y])
    """
    tracked_eye_center = eye_tracking.get_projected_center(input_data, RADIUS_3D_CIRCLE, FOCAL_LENGTH)
    if visualize:
        distance = np.linalg.norm(tracked_eye_center - PROJECTED_CENTER)

        plt.plot(PROJECTED_CENTER[0], PROJECTED_CENTER[1], marker='v')
        plt.show()
    return tracked_eye_center, distance


if __name__ == "__main__":
    input_data = simulate_input_data()
    reprojection(input_data, visualize=True)





