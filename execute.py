import projection
import numpy as np
import eye_tracking
import matplotlib.pyplot as plt


def gaze_maker(long_list, lat_list, radius):
    '''
    Combines every option of long and lat that is given
    :param long_list: list of spherical
    :param lat_list: list of spherical
    :param radius: single value
    :return: numpy array
    '''
    output = []
    for long in long_list:
        for lat in lat_list:
            output.append([long, lat, radius])
    return output


symmetric_30 = [[-30.0, -30.0, 0.2], [-30.0, 0.0, 0.2], [-30.0, 30.0, 0.2], [0.0, -30.0, 0.2], [0.0, 30.0, 0.2], [30.0, -30.0, 0.2], [30.0, 0.0, 0.2], [30.0, 30.0, 0.2]]
almost_symmetric_30 = [[-30.0, -30.0, 0.2], [-30.0, 0.1, 0.2], [-30.0, 30.0, 0.2], [0.1, -30.0, 0.2], [0.1, 30.0, 0.2], [30.0, -30.0, 0.2], [30.0, 0.1, 0.2], [30.0, 30.0, 0.2]]
####PARAMETERS################
EYE_CENTER = np.array([0.0, -5.0, 0.0])
SPHERE_RADIUS = 1.2
RESOLUTION = 100
RADIUS_3D_CIRCLE = 4
PUPIL_PARAM_LIST = almost_symmetric_30
FOCAL_LENGTH = 1
#TODO FOCAL LENGTH
#TODO RIGHT HANDED


if __name__ == "__main__":
    #Projection
    eye = projection.Eye(EYE_CENTER, SPHERE_RADIUS)
    ellipse_param_list = []
    for i in range(len(PUPIL_PARAM_LIST)):
        p = projection.Pupil(eye, PUPIL_PARAM_LIST[i], RESOLUTION)
        ellipse_param_list.append(p.get_ellipse_param_dict())

    #Unprojection
    results = eye_tracking.run(ellipse_param_list, RADIUS_3D_CIRCLE, FOCAL_LENGTH)

    real_projected_center = [EYE_CENTER[0]/-EYE_CENTER[1], EYE_CENTER[2]/-EYE_CENTER[1]]

    distance = np.linalg.norm(results - real_projected_center)
    print(distance)
    plt.plot(real_projected_center[0], real_projected_center[1], marker='v')
    plt.show()
