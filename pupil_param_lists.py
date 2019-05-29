"""
A module that contains and makes pupil_param lists
"""

symmetric_30 = [[-30.0, -30.0, 0.2], [-30.0, 0.1, 0.2], [-30.0, 30.0, 0.2], [0.1, -30.0, 0.2], [0.1, 30.0, 0.2], [30.0, -30.0, 0.2], [30.0, 0.1, 0.2], [30.0, 30.0, 0.2]]


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


degree_list = [-30.0, -15.0, 0.1, 15.0, 30.0]
symmetric_30_15 = gaze_maker(degree_list, degree_list, 0.15)
